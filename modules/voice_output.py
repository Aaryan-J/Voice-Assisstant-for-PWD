# voice_output.py
import pyttsx3
import time

def speak(text):
    """
    Speaks the given text using pyttsx3.
    Creates a new engine each time to avoid Windows SAPI5 run loop issues.
    Blocks until speech is finished.
    """
    if not text:
        return

    engine = pyttsx3.init('sapi5')  # fresh engine every time
    engine.setProperty('rate', 160)  # speech speed
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # ensures engine fully releases
    time.sleep(0.2)  # short pause to prevent overlap with next listen
