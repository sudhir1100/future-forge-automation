import argparse
import asyncio
import os
import sys
from src.utils import setup_logging, ensure_dir_exists
from src.llm_wrapper import LLMWrapper
from src.voice_engine import VoiceEngine
from src.asset_manager import AssetManager
from src.video_editor import VideoEditor
from src.youtube_uploader import YouTubeUploader

logger = setup_logging()

async def main():
    parser = argparse.ArgumentParser(description="Future Forge Automation Engine")
    parser.add_argument("--dry-run", action="store_true", help="Generate video but do not upload")
    parser.add_argument("--topic", type=str, help="Specific topic to generate")
    parser.add_argument("--type", type=str, choices=["long", "short"], default="long", help="Type of video to generate")
    parser.add_argument("--style", type=str, choices=["noir", "stickman"], default="noir", help="Visual style of the video")
    args = parser.parse_args()

    logger.info(f"Starting Daily Automation in {args.style} style...")
    ensure_dir_exists("temp")
    ensure_dir_exists("output")

    # 1. Generate Content
    llm = LLMWrapper()
    voice = VoiceEngine()
    
    from src.trends import TrendEngine
    trend_engine = TrendEngine()
    
    # Select Topic
    title = args.topic
    if not title:
        title = trend_engine.get_viral_topic(llm)
        if not title:
            logger.error("Failed to discover a viral topic")
            sys.exit(1)
        logger.info(f"Viral Topic Selected: {title}")
    
    # Override voice for stickman style if requested (Harry-like deep voice)
    if args.style == "stickman":
        voice.voice = "en-GB-RyanNeural" 
        logger.info(f"Using deep voice: {voice.voice}")
    
    logger.info(f"Generating {args.type} script for Title: {title}")
    
    if args.style == "stickman":
         script_data = llm.generate_conversational_script(title, type=args.type)
    elif args.type == "long":
        script_data = llm.generate_psychology_script(title)
    else:
        script_data = llm.generate_psychology_short_script(title)

    if not script_data:
        logger.error(f"Failed to generate {args.type} script")
        sys.exit(1)

    logger.info(f"Title: {script_data.get('title')}")
    if script_data.get('deduced_angle'):
        logger.info(f"Deduced Angle: {script_data.get('deduced_angle')}")
    
    # 2. Process Scenes
    asset_mgr = AssetManager()
    processed_scenes = []

    for i, scene in enumerate(script_data['scenes']):
        logger.info(f"Processing Scene {i+1}...")
        
        # Audio
        audio_path = f"temp/audio_{i}.mp3"
        await voice.generate_audio(scene['text'], audio_path)
        
        # Visuals
        # Use landscape for long-form, portrait for shorts
        orientation = "landscape" if args.type == "long" else "portrait"
        
        # Save visuals in persistent assets folder for tracking
        ensure_dir_exists("assets/visuals")
        video_path = f"assets/visuals/visual_{i}.jpg"
        
        prompt = scene.get('visual_prompt', scene.get('text'))
        logger.info(f"Generating Image with prompt: {prompt}")
        
        asset_mgr.generate_image(prompt, video_path, orientation=orientation)
        
        processed_scenes.append({
            'audio_path': audio_path,
            'video_path': video_path,
            'text': scene['text']
        })

    # 3. Create Video
    editor = VideoEditor()
    output_file = f"output/final_{args.type}.mp4"
    logger.info("Rendering video...")
    is_short = (args.type == "short")
    
    success = editor.create_video(processed_scenes, output_file, is_short=is_short, style=args.style)
    
    if success:
        logger.info(f"Video generated successfully: {output_file}")
    else:
        logger.error("Video generation failed")

    if not args.dry_run and success:
        # 4. Upload to YouTube
        logger.info("Starting Upload Process...")
        try:
            uploader = YouTubeUploader()
            
            # Generate Thumbnail
            ensure_dir_exists("assets/thumbnails")
            thumbnail_path = f"assets/thumbnails/thumb_{args.type}.jpg"
            logger.info(f"Generating Thumbnail for {title}...")
            asset_mgr.generate_thumbnail(title, thumbnail_path)

            description = script_data.get('description')
            if not description:
                description = f"{script_data.get('title')}\n\n#Psychology #Archetypes"
            
            video_id = uploader.upload_video(
                output_file, 
                script_data.get('title'), 
                description, 
                privacy_status="public"
            )

            if video_id and os.path.exists(thumbnail_path):
                uploader.set_thumbnail(video_id, thumbnail_path)
                logger.info(f"Successfully uploaded video and set thumbnail: https://youtu.be/{video_id}")
            elif video_id:
                logger.info(f"Successfully uploaded video: https://youtu.be/{video_id}")
        except Exception as e:
            logger.error(f"Upload process failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
