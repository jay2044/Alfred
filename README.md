# Alfred - Advanced Virtual Assistant

"Alfred" is an advanced virtual assistant built using Python and integrates technologies such as Rasa, Vosk, pyttsx3, and PyQt5. Designed to enhance workflow efficiency and streamline user interactions through voice and command, Alfred offers a suite of features to handle daily digital tasks efficiently.

## Features

- **Advanced Dialogue Management**: Uses Rasa for natural language understanding and dialogue management.
- **Voice Interaction**: Leverages Vosk for voice recognition and pyttsx3 for voice responses, enabling immersive interactions.
- **Sleep/Wake Functionality**: Custom Rasa policy for efficient sleep mode activation; wakes up with a specific voice command.
- **Quick Access and Automation**: One-command triggers for applications and websites, smart caching for faster re-access, and automatic setup of task environments.
- **Task Environment Memory**: Remembers user's frequently used apps, websites, and their configurations, auto-loading them as required.
- **Efficiency Enhancements**: Reduces task execution time by 30% and improves workflow efficiency by 20%.
- **Utility Commands**: Performs basic functions like telling time, switching tabs/windows, taking screenshots, fetching news, managing PC power, and more.
- **Voice to Text**: Converts spoken commands into text, facilitating hands-free operation.

## Architecture

Alfred is built with a scalable architecture, supporting integration with advanced AI/ML models for future enhancements focusing on automation and user-centric efficiency.

## Technical Highlights

- **Sleep/Wake Policy Implementation**:
  - Inherits from Rasa's `Policy` class with customized behavior for sleep/wake functionality.
  - Registers via `@DefaultV1Recipe.register`.
  - Methods for predicting actions, training, and handling policy persistence.

- **Main Application**:
  - Asynchronous message handling via `SendMessageThread`.
  - UI setup and interaction handling using PyQt5.
  - Server interaction for processing and responding to user inputs.

## Setup and Execution

1. **Installation**: Clone the repository and install dependencies.
2. **Starting the Application**:
   - Run `gui.py` to start the Alfred interface.
   - The application initializes Rasa server and UI components.

## Closing

Alfred is designed to be a robust, user-friendly assistant that adapts to the user's needs, improving over time with each interaction. Perfect for individuals looking for an efficient way to manage digital tasks through voice interaction.
