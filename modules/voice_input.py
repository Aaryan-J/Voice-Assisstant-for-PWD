import json
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def listen():
    # 1. Let Vosk auto-download and cache the model natively
    try:
        print("Initializing model (will download automatically on first run)...")
        model = Model(lang="en-us")
    except Exception as e:
        print(f"Error initializing Vosk model: {e}")
        return ""

    sample_rate = 16000
    recognizer = KaldiRecognizer(model, sample_rate)

    print("Listening...")

    timeout = 5
    phrase_limit = 5

    start_time = time.time()
    speech_started_time = None
    has_speech_started = False

    with sd.RawInputStream(samplerate=sample_rate, blocksize=4000, dtype='int16', channels=1) as stream:
        while True:
            data, overflowed = stream.read(4000)
            current_time = time.time()

            if not has_speech_started and (current_time - start_time > timeout):
                print("No speech detected.")
                return ""

            if has_speech_started and speech_started_time is not None and(current_time - speech_started_time > phrase_limit):
                print("Phrase time limit reached.")
                result_json = recognizer.FinalResult()
                break

            if recognizer.AcceptWaveform(bytes(data)):
                result_json = recognizer.Result()
                break
            else:
                partial_json = recognizer.PartialResult()
                partial_dict = json.loads(partial_json)
                if partial_dict.get("partial", "") != "":
                    if not has_speech_started:
                        has_speech_started = True
                        speech_started_time = time.time()

        try:
            result_dict = json.loads(result_json)
            text = result_dict.get("text", "").lower().strip()

            if text:
                print(f"You said: {text}")
                return text
            else:
                print("Sorry, I did not understand that.")
                return ""

        except Exception:
            print("Error parsing audio results.")
            return ""

if __name__ == "__main__":
    command = listen()
