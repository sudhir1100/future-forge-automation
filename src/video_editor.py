from moviepy.editor import *


import os

class VideoEditor:
    def create_video(self, scenes, output_path, is_short=True):
        """
        Stitches visualization, audio and subtitles.
        is_short: if True (9:16), if False (16:9)
        """
        # Target Dimensions
        if is_short:
            target_w, target_h = 1080, 1920
        else:
            target_w, target_h = 1920, 1080

        clips = []
        for scene in scenes:
            try:
                # Load Audio
                audio_clip = AudioFileClip(scene['audio_path'])
                duration = audio_clip.duration
                
                # Load Visual (Video OR Image)
                v_path = scene['video_path']
                if os.path.exists(v_path):
                    if v_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        # It's an image - Apply Zoom Animation
                        video_clip = ImageClip(v_path).set_duration(duration)
                        
                        # Apply subtle centered zoom-in effect (from 1.0 to 1.15)
                        # We resize first to ensure we have room to zoom without black bars
                        video_clip = video_clip.resize(height=target_h) if is_short else video_clip.resize(width=target_w)
                        video_clip = video_clip.resize(lambda t: 1.0 + 0.15 * (t/duration))
                        video_clip = video_clip.set_position('center')
                    else:
                        # It's a video
                        video_clip = VideoFileClip(v_path)
                        # Loop video if shorter than audio, or cut if longer
                        if video_clip.duration < duration:
                            video_clip = video_clip.loop(duration=duration)
                        else:
                            video_clip = video_clip.subclip(0, duration)
                else:
                    # Fallback to black screen if visual missing
                    video_clip = ColorClip(size=(target_w, target_h), color=(0,0,0), duration=duration)

                # Resize and crop to target aspect ratio
                # 1. Resize to fill the target dimensions (preserving aspect ratio)
                if video_clip.w / video_clip.h > target_w / target_h:
                    # Video is wider than target
                    video_clip = video_clip.resize(height=target_h)
                else:
                    # Video is taller than target
                    video_clip = video_clip.resize(width=target_w)
                
                # 2. Center crop
                video_clip = video_clip.crop(
                    x_center=video_clip.w/2, 
                    y_center=video_clip.h/2, 
                    width=target_w, 
                    height=target_h
                )
                
                # Set Audio
                video_clip = video_clip.set_audio(audio_clip)

                # Composite
                if is_short:
                    # Add Text Overlay (Simple Subtitle) for Shorts
                    txt_w = int(target_w * 0.8)
                    txt_clip = TextClip(
                        scene['text'], 
                        fontsize=70, 
                        color='white', 
                        font='Liberation-Sans-Bold', 
                        stroke_color='black', 
                        stroke_width=2, 
                        size=(txt_w, None), 
                        method='caption'
                    )
                    txt_clip = txt_clip.set_pos('center').set_duration(duration)
                    final_scene = CompositeVideoClip([video_clip, txt_clip])
                else:
                    # No text overlay for Long-form (Cinematic Style)
                    final_scene = video_clip
                
                clips.append(final_scene)
                
            except Exception as e:
                print(f"Error processing scene: {e}")
        
        if clips:
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", temp_audiofile="temp_audio.m4a")
            return True
        return False
