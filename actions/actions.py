# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import pyautogui
import pyperclip
import json
import threading
import subprocess
from datetime import datetime
import webbrowser

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionTypeMessage(Action):

    def name(self) -> Text:
        return "action_type_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the entity 'message_to_type' from the latest message
        message_to_type = next(tracker.get_latest_entity_values('message_to_type'), None)

        # If no 'message_to_type' was found, let the user know and return
        if message_to_type is None:
            dispatcher.utter_message(text="I didn't catch what I should type.")
            return []

        # Use pyautogui to type the message
        pyautogui.write(message_to_type, interval=0.05)
        dispatcher.utter_message(text="Message typed!")

        # Save the length of the last message typed in a slot
        return [SlotSet("last_message_length", len(message_to_type))]


class ActionRemoveMessage(Action):
    def name(self) -> Text:
        return "action_remove_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the length of the last message typed from the slot
        last_message_length = tracker.get_slot('last_message_length')

        # If no 'last_message_length' was found, let the user know and return
        if last_message_length is None:
            dispatcher.utter_message(text="There's no message to remove.")
            return []

        # Use pyautogui to perform a backspace operation the correct number of times
        for _ in range(last_message_length):
            pyautogui.press('backspace')
        dispatcher.utter_message(text="Message removed!")

        return []


class ActionPressEnterKey(Action):
    def name(self) -> Text:
        return "action_press_enter_key"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Use pyautogui to simulate pressing the 'enter' key
        pyautogui.press('enter')

        return []


class ActionCopyPaste(Action):
    def name(self) -> Text:
        return "action_copy_paste"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_message = tracker.latest_message.get('text').lower()

        if "copy" in last_message:
            # simulate "ctrl + c" which is the shortcut for "copy" operation
            pyautogui.hotkey('ctrl', 'c')
            dispatcher.utter_message(text="Message copied to clipboard!")
            return []

        elif "paste" in last_message:
            pyautogui.hotkey('ctrl', 'v')
            pasted_message = pyperclip.paste()
            dispatcher.utter_message(text="Message pasted from clipboard")
            return [SlotSet("last_message_length", len(pasted_message))]


class ActionOpenGoogle(Action):
    def name(self) -> Text:
        return "action_open_google"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.get_intent_of_latest_message()

        if intent == 'study':
            # Code to open Google in study profile
            dispatcher.utter_message(response="utter_open_study_profile")
            # Path to Chrome executable on Windows
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            # Command to open Chrome with the default profile
            command = f'"{chrome_path}" --profile-directory="Profile 1"'
            # Execute the command
            subprocess.Popen(command, shell=True)

        return []


class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_message = tracker.latest_message['text'].lower()

        if "time" in last_message and "date" in last_message:
            current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            dispatcher.utter_message(text=f"The current time and date is {current_datetime}.")
        elif "date" in last_message:
            current_date = datetime.now().strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Today's date is {current_date}.")
        elif "time" in last_message:
            current_time = datetime.now().strftime("%I:%M %p")
            dispatcher.utter_message(text=f"It is {current_time}.")

        return []


class ActionTakeScreenshot(Action):
    def name(self) -> Text:
        return "action_take_screenshot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(r"C:\Screenshots\screenshot.png")
            dispatcher.utter_message(text="Screenshot taken and saved")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while taking the screenshot: {str(e)}")

        return []


class ActionSleepMode(Action):
    def name(self):
        return "action_sleep_mode"

    def run(self, dispatcher, tracker, domain):
        print("sleep mode")
        return [SlotSet("is_asleep", True)]


class ActionWakeUp(Action):
    def name(self):
        return "action_wake_up"

    def run(self, dispatcher, tracker, domain):
        print("wake mode")
        return [SlotSet("is_asleep", False)]
