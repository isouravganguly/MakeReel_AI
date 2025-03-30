import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# Services Configuration
# --------------------------
SCRIPT_ENABLED = os.getenv("SCRIPT_ENABLED", "true").lower() == "true"
SCRIPT_PROVIDER = os.getenv("SCRIPT_PROVIDER", "gemini")

IMAGE_ENABLED = os.getenv("IMAGE_ENABLED", "true").lower() == "true"
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "gemini")

VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"
VOICE_PROVIDER = os.getenv("VOICE_PROVIDER", "elevenlabs")

# --------------------------
# Gemini Configuration
# --------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "dummy_api_key")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta")

# --------------------------
# ElevenLabs Configuration
# --------------------------
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "dummy_voice_key")
ELEVENLABS_VOICE_ID = os.getenv("VOICE_ID", "default_voice")
ELEVENLABS_API_URL = os.getenv("VOICE_API_URL", "https://api.elevenlabs.io/v1")

# --------------------------
# GetImgAI Configuration
# --------------------------
GETIMG_API_KEY = os.getenv("IMG_KEY", "dummy_image_key")
GETIMG_API_URL = os.getenv("IMAGE_API_URL", "https://api.getimg.ai/v1")

# --------------------------
# SunoAI Configuration
# --------------------------
SUNO_API_KEY = os.getenv("SUNO_API_KEY", "dummy_suno_key")
SUNO_API_URL = os.getenv("SUNO_API_URL", "https://api.suno.ai/v1")

SYSTEM_DOWNTIME = os.getenv("SYSTEM_DOWN_TIME", "false").lower() == "true"