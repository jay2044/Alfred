import json
import os
import subprocess
from rasa_sdk import Action, events, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActionExecuted
from typing import Any, Text, List, Dict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import webbrowser
from word2number import w2n


class ActionOpenApplication(Action):
    def name(self) -> Text:
        return "action_open_app_website"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        program_name = next(tracker.get_latest_entity_values('program_name'), None)
        print(program_name)
        if program_name is None:
            dispatcher.utter_message(text="I didn't catch what I should open.")
            return []

        try:
            # Check if the file exists, and if not, create an empty dictionary
            if not os.path.exists('program_list.json'):
                apps_and_websites = {}
            else:
                with open('program_list.json', 'r') as file:
                    apps_and_websites = json.load(file)

            # Match program_name using fuzzy matching
            top_matches = process.extract(program_name, apps_and_websites.keys(), limit=3)
            matched_app, score = top_matches[0]

            if score == 100:
                self.open(dispatcher, matched_app, apps_and_websites[matched_app])
            elif score > 85:
                options_text = "\n".join([f"{i + 1}. {match[0]}" for i, match in enumerate(top_matches)])
                message = f"Did you mean one of these? Please choose a number:\n{options_text}"
                dispatcher.utter_message(text=message)
                # Store the options in a slot for the next action to use
                return [SlotSet("program_options", [match[0] for match in top_matches])]
            else:
                dispatcher.utter_message(f"Unable to find {program_name}, Is it an app or website")
                return [SlotSet("program_name", program_name)]
        except json.JSONDecodeError:
            dispatcher.utter_message(f"An error occurred while reading the JSON file. Please check the file format.")
        except Exception as e:
            dispatcher.utter_message(f"Sorry, I dont understand what to open: {str(e)}")
        return []

    def open(self, dispatcher, name, info):
        try:
            if info['type'] == 'app':
                subprocess.run([info['path']])
            elif info['type'] == 'website':
                webbrowser.open(info['path'])  # Opens the website in the default browser
            dispatcher.utter_message(text=f"{name} opened successfully.")

            # Set the slots for program_name, program_type, and program_path
            return [
                SlotSet("program_name", name),
                SlotSet("program_type", info['type']),
                SlotSet("program_path", info['path'])
            ]
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while opening {name}: {str(e)}")
            return []


class ActionSpecifiedAppWebsite(Action):
    def name(self) -> Text:
        return "action_specified_app_website"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the type (app/website) and name
        type_ = next(tracker.get_latest_entity_values('program_type'), None)
        if type_ is None:
            type_ = tracker.get_slot("program_type")
        program_name = tracker.get_slot("program_name")
        program_path = None
        print(type_)

        # If it's a website, open it and ask to save the path
        if type_ == "website":
            try:
                program_path = f"https://www.{program_name}.com"
                webbrowser.open(program_path)
                dispatcher.utter_message(text=f"{program_name} opened successfully. Do you want to save this path?")
            except Exception as e:
                dispatcher.utter_message(text=f"An error occurred while opening {program_name}: {str(e)}")
        # If it's an app, ask to search directories
        elif type_ == "app":
            dispatcher.utter_message(text=f"Searched the directories for {program_name}?")
            # Define the directories you want to search
            search_directories = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users"]
            found_apps = []
            # Loop through the specified directories
            for directory in search_directories:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".exe"):
                            found_apps.append(os.path.join(root, file))
            # Fuzzy match the application name with the found executables
            top_matches = process.extract(program_name + ".exe", found_apps, limit=3, scorer=fuzz.partial_ratio)
            matched_app, score = top_matches[0]

            if score == 100:
                program_path = matched_app
                try:
                    subprocess.run([program_path])
                    dispatcher.utter_message(
                        text=f"{program_name} opened successfully. Do you want to save this path?")
                except Exception as e:
                    dispatcher.utter_message(text=f"An error occurred while opening {program_name}: {str(e)}")
            elif score > 80:
                # Get just the application names from the top matches
                app_names = [os.path.basename(match[0]) for match in top_matches]

                options_text = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(app_names)])
                message = f"Found the following results. Please choose a number:\n{options_text}"
                dispatcher.utter_message(text=message)
                # Store the application names in a slot for the next action to use
                return [SlotSet("program_options", app_names),
                        SlotSet("program_type", type_) if type_ else None]
            else:
                dispatcher.utter_message(text=f"Unable to find {program_name}.")
        return [
            SlotSet("program_name", program_name),
            SlotSet("program_type", type_),
            SlotSet("program_path", program_path) if program_path else None
        ]


class ActionChoseFromOptions(Action):
    def name(self) -> Text:
        return "action_chose_from_options"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve the user's chosen number
        chosen_number_text = next(tracker.get_latest_entity_values('chosen_number'), None)
        print(chosen_number_text)
        # Convert the chosen number text to an integer if it's a word
        try:
            if chosen_number_text in ["one", "first"]:
                chosen_number = 1
            elif chosen_number_text in ["two", "second"]:
                chosen_number = 2
            elif chosen_number_text in ["three", "third"]:
                chosen_number = 3

        except:
            dispatcher.utter_message(text=f"Sorry, I couldn't understand the number: {chosen_number_text}")
            return []

        # Retrieve the list of options from a previous slot or action
        options = tracker.get_slot("program_options")
        # Get the chosen option
        chosen_option = options[int(chosen_number) - 1]
        # Load previously opened applications and websites from JSON
        with open('program_list.json', 'r') as file:
            apps_and_websites = json.load(file)

        if chosen_option in apps_and_websites:
            # Open the chosen option based on type and path
            print("found")
            self.open(dispatcher, chosen_option, apps_and_websites[chosen_option])
        else:
            # Set the application_name to the chosen_option
            program_name = chosen_option.replace('.exe', '')
            print(program_name)
            # You can set a slot for application_name if needed
            return [SlotSet("program_name", program_name)]

        return []

    def open(self, dispatcher, name, info):
        try:
            if info['type'] == 'app':
                subprocess.run([info['path']])
            elif info['type'] == 'website':
                webbrowser.open(info['path'])  # Opens the website in the default browser
            dispatcher.utter_message(text=f"{name} opened successfully.")

            # Set the slots for program_name, program_type, and program_path
            return [
                SlotSet("program_name", name),
                SlotSet("program_type", info['type']),
                SlotSet("program_path", info['path'])
            ]
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while opening {name}: {str(e)}")
            return []


class ActionSaveToFile(Action):
    def name(self) -> Text:
        return "action_save_to_file"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program_name = tracker.get_slot("program_name")
        program_type = tracker.get_slot("program_type")
        program_path = tracker.get_slot("program_path")

        # Construct the new entry
        new_entry = {
            "name": program_name,
            "type": program_type,
            "path": program_path
        }

        # Read the existing entries
        try:
            with open('program_list.json', 'r') as file:
                apps_and_websites = json.load(file)
        except FileNotFoundError:
            apps_and_websites = {}

        # Add the new entry with the name as the key
        apps_and_websites[program_name] = new_entry

        # Write back to the file
        with open('program_list.json', 'w') as file:
            json.dump(apps_and_websites, file)

        dispatcher.utter_message(text=f"{program_name} has been saved successfully.")
        return []
