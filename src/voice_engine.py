import edge_tts
import asyncio
from .config import Config

class VoiceEngine:
    def __init__(self):
        self.voice = Config.VOICE_NAME

    async def generate_audio(self, text, output_file):
        """
        Generates speech from text using MS Edge TTS.
        """
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_file)
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False
