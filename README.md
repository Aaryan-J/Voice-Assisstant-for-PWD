# Offline Voice Assistant for PWD

## Description
An offline, terminal-based voice assistant designed for privacy, accessibility, and modularity. It allows users to take notes, set reminders, and perform basic tasks entirely offline. The system is built to be easily extendable, so additional features can be integrated seamlessly in the future.

## Features
- **Offline Voice Commands**: Fully functional without an internet connection.
- **Note Taking via Voice**: Quickly capture ideas or reminders using speech.
- **Reminder Setting**: Set and receive reminders through voice commands.
- **Modular Architecture**: Easily extendable to add new features, commands, or integrations.
- **Terminal-Based Interaction**: Lightweight, low-resource interface suitable for all systems.

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/Aaryan-J/Voice-Assisstant-for-PWD.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the assistant:
```bash
python main.py
```

## Usage
Start the program and speak commands into your microphone.
Example commands:
“Take note: Buy groceries tomorrow”
“Set reminder for 7 PM: Study Python”
“Show my notes”
Notes and reminders are stored locally, maintaining full privacy.

## Modularity & Extensibility
- Each feature is implemented as a separate module, making it easy to add new capabilities.
- Developers can create additional modules for tasks such as:
- Calendar management
- Local file operations
- Music or media control

## Contributing
Contributions are welcome! Add new modules, improve voice recognition, or suggest enhancements. Please follow standard Python practices and document any new module added.
