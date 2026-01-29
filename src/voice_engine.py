import edge_tts
import asyncio
from .config import Config

class VoiceEngine:
    def __init__(self):
        self.voice = Config.VOICE_NAME

    async def generate_audio(self, text, output_file, mood="neutral"):
        """
        Generates speech from text using MS Edge TTS with emotional parameters.
        Moods: neutral, excited, serious, whispering, curious
        """
        try:
            # Clean text: Remove markdown emphasis and asterisks
            import re
            clean_text = re.sub(r'[*_#~>]', '', text)
            
            # Map moods to edge-tts parameters
            # Rate: +X% (faster), -X% (slower)
            # Pitch: +XHz (higher), -XHz (lower)
            mood_params = {
                "excited": {"rate": "+10%", "pitch": "+2Hz"},
                "serious": {"rate": "-5%", "pitch": "-2Hz"},
                "whispering": {"rate": "-10%", "pitch": "-5Hz"},
                "curious": {"rate": "+0%", "pitch": "+2Hz"},
                "neutral": {"rate": "+0%", "pitch": "+0Hz"}
            }
            
            params = mood_params.get(mood.lower(), mood_params["neutral"])
            
            communicate = edge_tts.Communicate(
                clean_text, 
                self.voice, 
                rate=params["rate"], 
                pitch=params["pitch"]
            )
            await communicate.save(output_file)
            
            # Post-processing: Remove silence
            self._remove_silence(output_file)
            
            return True
        except Exception as e:
            print(f"Error generating audio with mood {mood}: {e}")
            return False

    def _remove_silence(self, file_path):
        """Removes long silences using FFmpeg."""
        import subprocess
        import os
        from imageio_ffmpeg import get_ffmpeg_exe
        
        ffmpeg_exe = get_ffmpeg_exe()
        
        temp_path = file_path.replace(".mp3", "_temp.mp3")
        # silenceremove=start_periods=1:start_duration=0:start_threshold=-40dB:stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB
        # Removes silence at start and any silence > 0.5s in the middle/end
        command = [
            ffmpeg_exe, "-y", "-i", file_path,
            "-af", "silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-45dB",
            temp_path
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(temp_path):
                os.replace(temp_path, file_path)
        except Exception as e:
            print(f"Warning: Could not remove silence (ffmpeg might be missing): {e}")
