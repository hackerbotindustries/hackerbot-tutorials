import time
import google.generativeai as genai
from hackerbot import Hackerbot
from utils import *
import speech_recognition as sr
from dotenv import load_dotenv
import os

def ask_gemini(model, prompt):
    """Send user input to Gemini and get response."""
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.3,
        )
    )
    return response.text

def main():
    """
    Main function of the robot assistant.

    This function initializes the robot assistant, which consists of the following steps:

    1. Load environment variables
    2. Configure Gemini API
    3. Initialize Speech Recognition and Hackerbot
    4. Main loop, listening to user input and sending it to Gemini

    The main loop:

    1. Listens to user input using speech recognition
    2. Sends the user input to Gemini
    3. Handles the Gemini response
    4. Waits for a short period of time before the next cycle

    The robot assistant can be stopped by pressing Ctrl+C.
    """
    # 1. Load environment variables
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

    # 2. Configure Gemini API
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [{"text": 
                # Configure Personality
                "You are a colleague named Robby, and you are experiencing Monday blues.\n"
                # Configure Response Format
                "Respond ONLY with JSON string (not Python dicts or lists) in one of the following formats:\n" 
                "- {\"action\": \"action_name\"}\n"
                "- {\"action\": \"speak\", \"parameters\": {\"text\": \"your text\"}}\n"
                "- or a list of such objects if you want the robot to perform multiple actions.\n\n"
                "If you want the robot to MOVE and SPEAK at the same time, "
                "include both actions together in the list (speaking will be handled in a separate thread).\n\n"
                # Configure Actions, add new actions here
                "Supported actions are: shake_head, nod_head, look_left, look_right, look_up, look_down, spin_right, spin_left, spin_around, and speak.\n\n"
                "DO NOT add any extra explanation.\n"
                "DO NOT use markdown formatting like triple backticks.\n"
                "ONLY reply with pure raw JSON."
            }]
        },
        {
            "role": "model",
            "parts": [{"text": "Understood. I will only respond with raw JSON without explanations or formatting."}]
        }
    ])
    # Initialize Speech Recognition and Hackerbot
    recognizer = sr.Recognizer()
    bot = Hackerbot()
    
    try:
        # Main loop, listening to user input and sending it to Gemini
        print("Robot Assistant Started. Press Ctrl+C to stop.")
        while True:
            user_input = listen_to_user(recognizer)
            if not user_input:
                continue

            prompt = f"Here is the user input:\n\n{user_input}"

            gemini_response = chat.send_message(prompt)
            handle_response(bot, extract_json_from_response(gemini_response.text))
            time.sleep(1)  # Small delay between cycles

    except KeyboardInterrupt:
        print("Robot Assistant Stopped.")
    finally:
        # Cleanup
        bot.base.destroy()

if __name__ == "__main__":
    main()
