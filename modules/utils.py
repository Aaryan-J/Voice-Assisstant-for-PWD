from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"
VOICE_DIR = ASSETS_DIR / "voice"

DATA_DIR.mkdir(exist_ok=True)
VOICE_DIR.mkdir(parents=True, exist_ok=True)

def get_data_path(filename: str) -> Path:
    return DATA_DIR / filename

def get_asset_path(filename: str) -> Path:
    return ASSETS_DIR / filename

def get_voice_path(filename: str) -> Path:
    return VOICE_DIR / filename
