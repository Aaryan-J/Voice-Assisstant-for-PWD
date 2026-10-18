# Offline Voice Assistant for PWD

## Description
An offline, terminal-based voice assistant designed for privacy, accessibility, and modularity. It allows users to take notes, set reminders, and perform basic tasks entirely offline. The system is built to be easily extendable, so additional features can be integrated seamlessly in the future.

## Features
- **Offline Voice Commands**: Fully functional without an internet connection.
- **Note Taking via Voice**: Quickly capture ideas or reminders using speech.
- **Reminder Setting**: Set and receive reminders through voice commands.
- **Modular Architecture**: Easily extendable to add new features, commands, or integrations.
- **Terminal-Based Interaction**: Lightweight, low-resource interface suitable for all systems.

## Tech Stack
| Component | Library | Notes |
|---|---|---|
| **Speech-to-Text** | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Offline, CTranslate2-based. Uses the `tiny.en` model (~75 MB) for fast, accurate command recognition. Auto-downloads on first run. |
| **Text-to-Speech** | [piper-tts](https://github.com/rhasspy/piper) | Offline neural TTS. Voice files stored in `assets/voice/`. |
| **Audio I/O** | [sounddevice](https://github.com/spatialaudio/python-sounddevice) | Low-latency cross-platform mic input and playback. |

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/Aaryan-J/Voice-Assisstant-for-PWD.git
cd Voice-Assistant-for-PWD
```
2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```
3. Download the Piper voice files (one-time) into `assets/voice/`:
   - [en_US-amy-medium.onnx](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx)
   - [en_US-amy-medium.onnx.json](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json)
4. Ensure `assets/alarms.wav` exists for reminder alarms (a default beep is bundled).

## How to Run
The dependencies live in the project `venv/`, so plain `python main.py` (system Python) will fail with `ModuleNotFoundError`. Use one of these instead:

**Option A — `run.py` (recommended, works anywhere):**
```bash
python run.py
```
This detects the `venv/` and re-execs into it automatically, regardless of which `python` is on your PATH.

**Option B — activate the venv first:**
```bash
source venv/bin/activate
python main.py
```

**In Zed / VS Code:** editors that auto-detect `venv/` (Zed does by default) will activate it in their integrated terminal, so `python main.py` works there directly after a fresh editor restart.

> The `tiny.en` Whisper model (~75 MB) will auto-download to the Hugging Face cache on first run. After that, everything works fully offline.

## Usage
- Start the program and speak commands into your microphone.
- Example commands:
  - “Take note: Buy groceries tomorrow”
  - “Set reminder for 7 PM: Study Python”
  - “Show my notes”
- Notes and reminders are stored locally, maintaining full privacy.

## Modularity & Extensibility
- Each feature is implemented as a separate module, making it easy to add new capabilities.
- Developers can create additional modules for tasks such as:
  - Calendar management
  - Local file operations
  - Music or media control

## Contributing
Contributions are welcome! Add new modules, improve voice recognition, or suggest enhancements. Please follow standard Python practices and document any new module added.
