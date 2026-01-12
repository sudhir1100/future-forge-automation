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
            # Clean text: Remove markdown emphasis and asterisks that TTS might read aloud
            import re
            clean_text = re.sub(r'[*_#~>]', '', text)
            
            communicate = edge_tts.Communicate(clean_text, self.voice)
            await communicate.save(output_file)
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False
