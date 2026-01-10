import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    
    # YouTube Auth
    YOUTUBE_CLIENT_SECRET_FILE = "client_secrets.json"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    # Content Settings
    NICHE = "Future Tech and Artificial Intelligence"
    VIDEO_LANGUAGE = "en-US"
    VOICE_NAME = "en-US-ChristopherNeural" # Deep, professional male voice
