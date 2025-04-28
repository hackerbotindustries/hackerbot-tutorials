import os
import json
import time
import speech_recognition as sr
import google.generativeai as genai
from hackerbot import Hackerbot
from hackerbot_actions import *
import threading


# ====== SETUP ======

# 1. Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAH6-MMvC552PE2YrVgOI1h6JUkc-_UPqM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# 2. Initialize Speech Recognizer
recognizer = sr.Recognizer()

bot = Hackerbot()

# ====== FUNCTIONS ======

def listen_to_user():
    """Capture microphone input and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

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

def handle_gemini_response(response_text):
    try:
        response_json = json.loads(response_text)
        print("Received JSON response:", response_json)
        if isinstance(response_json, list):
            for action_obj in response_json:
                action = action_obj.get("action")
                parameters = action_obj.get("parameters", {})
                if action:
                    execute_robot_action(action, parameters)
                else:
                    print("One action object does not contain 'action'.")
        else:
            action = response_json.get("action")
            parameters = response_json.get("parameters", {})
            if action:
                execute_robot_action(action, parameters)
            else:
                print("JSON response does not contain 'action'.")
    except json.JSONDecodeError:
        print("Received non-JSON response:", response_text)

def execute_robot_action(action, parameters):
    print(f"Executing action: {action}")
    action_map = {
        "shake_head": lambda: shake_head(bot),
        "nod_head": lambda: nod_head(bot),
        "look_left": lambda: look_left(bot),
        "look_right": lambda: look_right(bot),
        "look_up": lambda: look_up(bot),
        "look_down": lambda: look_down(bot),
        "spin_right": lambda: spin_right(bot),
        "spin_left": lambda: spin_left(bot),
        "spin_around": lambda: spin_around(bot),
        "speak": lambda: speak(bot, parameters.get("text")),
    }
    func = action_map.get(action)
    if func:
        if action == "speak":
            # Run speaking in a separate thread
            threading.Thread(target=func).start()
        else:
            # Movements happen normally (you can also thread them if you want simultaneous moves)
            func()
    else:
        print(f"Unknown action: {action}")

# ====== MAIN LOOP ======

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
            handle_gemini_response(gemini_response)
            time.sleep(1)  # Small delay between cycles

    except KeyboardInterrupt:
        print("Robot Assistant Stopped.")
    finally:
        bot.base.destroy()

if __name__ == "__main__":
    main()
