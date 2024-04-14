# Alfred - Advanced Virtual Assistant

Alfred is an AI assistant developed using Python, Rasa, Vosk, pyttsx3, and PyQt5. It offers advanced natural language understanding and dialogue management, with over 20 unique features to enhance user productivity and convenience.

## Features

- **Sleep Mode**: Alfred activates on command or when prompted, enhancing conversational dynamics.
- **One-Command Access**: Instantly open applications/websites and automate task environment setup.
- **Immersive Voice Interaction**: Utilizes Vosk and pyttsx3 for seamless voice-based interaction.
- **Task Environment**: Saves data of frequently performed tasks, enabling quick access and configuration.
- **Efficient Rasa Policy**: Implements a custom policy for intelligent sleep/wake functionality.

## Actions

- **Wake and Sleep Mode**: Alfred wakes up upon hearing "Alfred" and returns to sleep after interaction.
- **Immersive Responses**: Engaging voice responses for a more natural interaction.
- **Application and Website Opening**: Open any application or website with a single command.
- **Cached Access**: Remembers frequently used apps/websites for instant access.
- **Basic Commands**: Perform various tasks like time/date check, tab/window switching, taking screenshots, news updates, and PC power control.
- **Voice Recognition Typing**: Allows for voice recognition-based typing.

## Sleep/Wake Policy Implementation

- Inherits from Rasa's Policy class.
- Registered using @DefaultV1Recipe.register.
- **Methods**: Handles action prediction, customization, training logic, and persistence.
- **Type Annotations**: Utilizes typing module for specifying types.
- **Conditional Logic**: Determines action based on tracker state.
- **Integration**: Interacts with Rasa components for seamless functionality.

## Main Code Structure

- **Import Statements**: Necessary modules like sys, subprocess, PyQt5, requests, etc.
- **Class Definitions**: Defines SendMessageThread and ChatApplication classes.
- **Initialization**: Sets up UI, starts Rasa server, and sets timer for server status.
- **UI Setup**: Creates UI elements using PyQt5 widgets.
- **Functionality**: Methods for sending/receiving messages, toggling mic, TTS functionality.
- **Event Handling**: Handles application closing event.
- **Execution**: Runs the PyQt5 application.

## Usage

1. Sry WIP
   
## Contributors

- me

## License

This project is licensed under nothing yet 😔. See the LICENSE file for details.


