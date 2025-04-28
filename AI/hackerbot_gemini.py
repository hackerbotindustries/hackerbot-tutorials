import time
import google.generativeai as genai
from hackerbot import Hackerbot
from AI_utils import *


# ====== SETUP ======

# 1. Configure Gemini API
# GOOGLE_API_KEY = "AIzaSyAH6-MMvC552PE2YrVgOI1h6JUkc-_UPqM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

bot = Hackerbot()

def ask_gemini(prompt):
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
    try:
        print("Robot Assistant Started. Press Ctrl+C to stop.")
        while True:
            user_input = listen_to_user()
            if not user_input:
                continue
            # Customize the prompt you send to Gemini
            prompt = (
                "You are a robot controller. "
                "Respond ONLY with JSON in one of the following formats: "
                "either a single object like {\"action\": \"action_name\"} or {\"action\": \"speak\", \"parameters\": {\"text\": \"your text\"}}, "
                "or a list of such objects if you want the robot to perform multiple actions. "
                "If you want the robot to MOVE and SPEAK at the same time, "
                "include both actions together in the list — speaking will be handled in a separate thread. "
                "Supported actions are: shake_head, nod_head, look_left, look_right, look_up, look_down, spin_right, spin_left, spin_around, and speak. "
                "ONLY respond with JSON. "
                "Here is the user input:\n\n"
                f"{user_input}"
            )
            gemini_response = ask_gemini(prompt)
            handle_response(gemini_response)
            time.sleep(1)  # Small delay between cycles

    except KeyboardInterrupt:
        print("Robot Assistant Stopped.")
    finally:
        bot.base.destroy()

if __name__ == "__main__":
    main()
