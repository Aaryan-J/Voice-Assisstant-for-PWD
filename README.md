# Offline Voice Assistant for PWD

## Description
An offline, terminal-based voice assistant designed for privacy, accessibility, and modularity. It allows users to take notes, set reminders, and perform basic tasks entirely offline. The system is built to be easily extendable, so additional features can be integrated seamlessly in the future.

## Features
- **Fully Offline**: Works without an internet connection — built for privacy and accessibility (PWD).
- **Note Taking via Voice**: Quickly capture ideas or reminders using speech.
- **Date-Aware Reminders**: Set reminders for a time or a specific day ("tomorrow at 3 PM", "Monday at 9 AM"). Confirmed aloud so you can verify.
- **Time & Date Queries**: Ask "what time is it", "what's the date", or "what day is it".
- **Offline Calculator**: Ask "what is 42 times 7" — understands spoken numbers and word operators.
- **Modular Command Registry**: Each feature is a self-contained handler, making it easy to add new commands.
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
  - "Make a note: buy groceries tomorrow"
  - "Read my notes"
  - "Set a reminder to take medicine" → then "tomorrow at 3 PM"
  - "What time is it?"
  - "What is 42 times 7?"
  - "Exit"
- Notes and reminders are stored locally, maintaining full privacy.

## Modularity & Extensibility
- Each feature is a command handler in `modules/commands/`, registered through `modules/registry.py`.
- To add a command, create a `Handler` subclass with `match()` (returns a confidence score) and `run()`, then register it in `modules/commands/__init__.py`.
- Ideas for future commands: calendar (ICS) management, local file operations, music/media control.

## Contributing
Contributions are welcome! Add new modules, improve voice recognition, or suggest enhancements. Please follow standard Python practices and document any new module added.
