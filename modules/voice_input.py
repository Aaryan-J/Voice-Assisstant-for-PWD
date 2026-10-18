import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOCK_SIZE = 4000
TIMEOUT = 5.0
PHRASE_LIMIT = 8.0
ENERGY_THRESHOLD = 0.01
SILENCE_TAIL = 1.2

_model = None
_model_error = False

def _get_model() -> WhisperModel | None:
    global _model, _model_error
    if _model is not None:
        return _model
    if _model_error:
        return None
    try:
        _model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    except Exception as e:
        _model_error = True
        print(f"Error: Could not load Whisper model ({e}).")
        print("Connect to the internet once so it can download, then re-run.")
        return None
    return _model

def listen() -> str:
    model = _get_model()
    if model is None:
        return ""

    try:
        stream_ctx = sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            dtype="float32",
        )
    except Exception as e:
        print(f"Error: No microphone detected ({e}).")
        return ""

    start_time = time.time()
    has_speech = False
    speech_start = 0.0
    last_speech = 0.0
    audio_frames = []

    with stream_ctx as stream:
        while True:
            data, _ = stream.read(BLOCK_SIZE)
            audio_frames.append(data.flatten())
            rms = float(np.sqrt(np.mean(data ** 2)))
            now = time.time()

            if rms > ENERGY_THRESHOLD:
                if not has_speech:
                    has_speech = True
                    speech_start = now
                last_speech = now

            if has_speech:
                if (now - last_speech) > SILENCE_TAIL:
                    break
                if (now - speech_start) > PHRASE_LIMIT:
                    break
            else:
                if (now - start_time) > TIMEOUT:
                    print("No speech detected.")
                    return ""

    audio = np.concatenate(audio_frames).astype(np.float32)
    segments, _ = model.transcribe(audio, beam_size=5, vad_filter=True)
    text = " ".join(seg.text.strip() for seg in segments).strip().lower()

    if text:
        print(f"You said: {text}")
        return text

    print("Sorry, I did not understand that.")
    return ""
