from moviepy.editor import *


import os

class VideoEditor:
    def create_video(self, scenes, output_path, is_short=True, bg_music_path=None):
        """
        Stitches visualization, audio and subtitles with dynamic animations and transitions.
        is_short: if True (9:16), if False (16:9)
        """
        # Target Dimensions
        if is_short:
            target_w, target_h = 1080, 1920
        else:
            target_w, target_h = 1920, 1080

        import random
        clips = []
        for i, scene in enumerate(scenes):
            try:
                # Load Audio
                audio_clip = AudioFileClip(scene['audio_path'])
                duration = audio_clip.duration
                
                # Load Visual (Video OR Image)
                v_path = scene['video_path']
                if os.path.exists(v_path):
                    if v_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        # It's an image - Apply Robust Ken Burns Effect
                        img_clip = ImageClip(v_path).set_duration(duration)
                        
                        # Select random animation
                        anim_type = random.choice(['zoom_in', 'zoom_out', 'pan_left', 'pan_right'])
                        
                        # For Ken Burns, start with a clip slightly larger than target
                        # to avoid black edges during pan/zoom
                        base_scale = 1.3
                        
                        if is_short:
                            img_clip = img_clip.resize(height=int(target_h * base_scale))
                        else:
                            img_clip = img_clip.resize(width=int(target_w * base_scale))
                            
                        # Centered Crop as base
                        img_clip = img_clip.crop(
                            x_center=img_clip.w/2, 
                            y_center=img_clip.h/2, 
                            width=int(target_w * 1.1), 
                            height=int(target_h * 1.1)
                        )
                        
                        # Apply dynamic animation
                        if anim_type == 'zoom_in':
                            video_clip = img_clip.resize(lambda t: 1.0 + 0.15 * (t/duration))
                        elif anim_type == 'zoom_out':
                            video_clip = img_clip.resize(lambda t: 1.15 - 0.15 * (t/duration))
                        elif anim_type == 'pan_left':
                            # Dynamic position for pan
                            video_clip = img_clip.set_position(lambda t: (int(-0.1 * target_w * (t/duration)), 'center'))
                        elif anim_type == 'pan_right':
                            video_clip = img_clip.set_position(lambda t: (int(-0.1 * target_w * (1 - t/duration)), 'center'))
                        else:
                            video_clip = img_clip
                            
                        # Final resize to fit target exactly (if needed) and ensure it's centered
                        if anim_type.startswith('zoom'):
                            video_clip = video_clip.set_position('center')
                        
                        # Ensure we crop to target dimensions
                        video_clip = video_clip.crop(x_center=video_clip.w/2, y_center=video_clip.h/2, width=target_w, height=target_h)

                    else:
                        # It's a video
                        video_clip = VideoFileClip(v_path)
                        if video_clip.duration < duration:
                            video_clip = video_clip.loop(duration=duration)
                        else:
                            video_clip = video_clip.subclip(0, duration)
                        
                        # Consistent resize/crop for video
                        if video_clip.w / video_clip.h > target_w / target_h:
                            video_clip = video_clip.resize(height=target_h)
                        else:
                            video_clip = video_clip.resize(width=target_w)
                        video_clip = video_clip.crop(x_center=video_clip.w/2, y_center=video_clip.h/2, width=target_w, height=target_h)
                else:
                    video_clip = ColorClip(size=(target_w, target_h), color=(0,0,0), duration=duration)

                video_clip = video_clip.set_audio(audio_clip)

                # Add Crossfade Transition (except for the first clip)
                if i > 0:
                    video_clip = video_clip.crossfadein(0.5)

                # Composite
                if is_short:
                    # Minimalist Cinematic Subtitles for Shorts
                    txt_w = int(target_w * 0.9)
                    txt_clip = TextClip(
                        scene['text'], 
                        fontsize=50, 
                        color='white', 
                        font='Arial-Bold', 
                        stroke_color='black', 
                        stroke_width=1, 
                        size=(txt_w, None), 
                        method='caption'
                    )
                    # Position at the very bottom with slight padding
                    txt_clip = txt_clip.set_pos(('center', target_h * 0.85)).set_duration(duration)
                    final_scene = CompositeVideoClip([video_clip, txt_clip])
                else:
                    # Minimalist Subtitles for Long-form (Optional, but user asked for better experience)
                    # We'll use a very subtle bottom subtitle
                    txt_w = int(target_w * 0.8)
                    txt_clip = TextClip(
                        scene['text'], 
                        fontsize=40, 
                        color='white', 
                        font='Arial', 
                        size=(txt_w, None), 
                        method='caption'
                    )
                    txt_clip = txt_clip.set_pos(('center', target_h * 0.9)).set_duration(duration)
                    final_scene = CompositeVideoClip([video_clip, txt_clip])
                
                clips.append(final_scene)
                
            except Exception as e:
                print(f"Error processing scene: {e}")
        
        if clips:
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Add Background Music if provided
            if bg_music_path and os.path.exists(bg_music_path):
                bg_audio = AudioFileClip(bg_music_path).volumex(0.08) # Lower volume (8%) for richer voiceover clarity
                if bg_audio.duration < final_video.duration:
                    bg_audio = bg_audio.loop(duration=final_video.duration)
                else:
                    bg_audio = bg_audio.subclip(0, final_video.duration)
                
                final_audio = CompositeAudioClip([final_video.audio, bg_audio])
                final_video = final_video.set_audio(final_audio)

            final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", temp_audiofile="temp_audio.m4a", threads=4)
            return True
        return False
