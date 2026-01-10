from moviepy.editor import *


import os

class VideoEditor:
    def create_video(self, scenes, output_path):
        """
        Stitches visualization, audio and subtitles.
        scenes: List of dicts with 'video_path', 'audio_path', 'text'
        """
        clips = []
        for scene in scenes:
            try:
                # Load Audio
                audio_clip = AudioFileClip(scene['audio_path'])
                duration = audio_clip.duration
                
                # Load Video
                if os.path.exists(scene['video_path']):
                    video_clip = VideoFileClip(scene['video_path'])
                    # Loop video if shorter than audio, or cut if longer
                    if video_clip.duration < duration:
                        video_clip = video_clip.loop(duration=duration)
                    else:
                        video_clip = video_clip.subclip(0, duration)
                else:
                    # Fallback to black screen if video missing
                    video_clip = ColorClip(size=(1080, 1920), color=(0,0,0), duration=duration)

                # Resize to 9:16 aspect ratio (Vertical)
                # target: 1080x1920
                video_clip = video_clip.resize(height=1920)
                if video_clip.w < 1080:
                     video_clip = video_clip.resize(width=1080)
                video_clip = video_clip.crop(x1=video_clip.w/2-540, y1=video_clip.h/2-960, width=1080, height=1920)
                
                # Set Audio
                video_clip = video_clip.set_audio(audio_clip)

                # Add Text Overlay (Simple Subtitle)
                txt_clip = TextClip(scene['text'], fontsize=70, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2, size=(800, None), method='caption')
                txt_clip = txt_clip.set_pos('center').set_duration(duration)
                
                # Composite
                final_scene = CompositeVideoClip([video_clip, txt_clip])
                clips.append(final_scene)
                
            except Exception as e:
                print(f"Error processing scene: {e}")
        
        if clips:
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
            return True
        return False
