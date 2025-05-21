import os
import json
import speech_recognition as sr
from actions import *
import re

def extract_json_from_response(response_text):
    """Extract clean JSON from a possible markdown-wrapped response."""
    if response_text.startswith("```"):
        # Remove triple backticks and optional "json" marker
        response_text = re.sub(r"^```(?:json)?\n?", "", response_text)
        response_text = re.sub(r"\n?```$", "", response_text)
    return response_text.strip()

def listen_to_user(recognizer):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text, None
    except sr.UnknownValueError:
        return None, "Speech was unintelligible."
    except sr.RequestError as e:
        return None, f"API request failed: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"

def handle_response(bot, response_text):
    try:
        response_json = json.loads(response_text)
        print("Received JSON response:", response_json)
        if isinstance(response_json, list):
            for action_obj in response_json:
                action = action_obj.get("action")
                parameters = action_obj.get("parameters", {})
                if action:
                    execute_robot_action(bot, action, parameters)
                else:
                    print("One action object does not contain 'action'.")
        else:
            action = response_json.get("action")
            parameters = response_json.get("parameters", {})
            if action:
                execute_robot_action(bot, action, parameters)
            else:
                print("JSON response does not contain 'action'.")
    except json.JSONDecodeError:
        print("Received non-JSON response:", response_text)


def execute_robot_action(bot, action, parameters):
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
        # Movements happen normally (you can also thread them if you want simultaneous moves)
        func()
    else:
        print(f"Unknown action: {action}")