import json
import numpy as np
import sounddevice as sd
from piper import PiperVoice
from .utils import get_voice_path

_voice = None
_sample_rate = 22050
_voice_error = False

def _get_voice() -> PiperVoice | None:
    global _voice, _sample_rate, _voice_error
    if _voice is not None:
        return _voice
    if _voice_error:
        return None
    model_path = get_voice_path("en_US-amy-medium.onnx")
    config_path = get_voice_path("en_US-amy-medium.onnx.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        _sample_rate = config.get("audio", {}).get("sample_rate", 22050)
        _voice = PiperVoice.load(str(model_path), config_path=str(config_path))
    except Exception as e:
        _voice_error = True
        print(f"Error: Could not load Piper voice ({e}).")
        print("Download en_US-amy-medium.onnx and en_US-amy-medium.onnx.json")
        print("into assets/voice/ (see README), then re-run.")
        return None
    return _voice

def speak(text: str) -> None:
    if not text:
        return
    voice = _get_voice()
    if voice is None:
        return
    chunks = list(voice.synthesize(text))
    audio_bytes = b"".join(c.audio_int16_bytes for c in chunks)
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
    sd.play(audio_np, samplerate=_sample_rate)
    sd.wait()
