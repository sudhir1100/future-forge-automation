import argparse
import asyncio
import os
from src.utils import setup_logging, ensure_dir_exists
from src.llm_wrapper import LLMWrapper
from src.voice_engine import VoiceEngine
from src.asset_manager import AssetManager
from src.video_editor import VideoEditor

logger = setup_logging()

async def main():
    parser = argparse.ArgumentParser(description="Future Forge Automation Engine")
    parser.add_argument("--dry-run", action="store_true", help="Generate video but do not upload")
    parser.add_argument("--topic", type=str, help="Specific topic to generate")
    args = parser.parse_args()

    logger.info("Starting Daily Automation...")
    ensure_dir_exists("temp")
    ensure_dir_exists("output")

    # 1. Generate Content
    llm = LLMWrapper()
    
    topic = args.topic if args.topic else "The Future of Quantum Computing" # Default or fetch from history
    logger.info(f"Generating script for topic: {topic}")
    
    script_data = llm.generate_script(topic)
    if not script_data:
        logger.error("Failed to generate script")
        return

    logger.info(f"Title: {script_data.get('title')}")
    
    # 2. Process Scenes
    voice = VoiceEngine()
    asset_mgr = AssetManager()
    processed_scenes = []

    for i, scene in enumerate(script_data['scenes']):
        logger.info(f"Processing Scene {i+1}...")
        
        # Audio
        audio_path = f"temp/audio_{i}.mp3"
        await voice.generate_audio(scene['text'], audio_path)
        
        # Visuals
        video_url = asset_mgr.search_video(scene['visual_keyword'])
        video_path = f"temp/video_{i}.mp4"
        if video_url:
            asset_mgr.download_file(video_url, video_path)
        else:
            logger.warning(f"No video found for {scene['visual_keyword']}")
            # Create dummy black video or handle fallback later (VideoEditor handles missing files)
        
        processed_scenes.append({
            'audio_path': audio_path,
            'video_path': video_path,
            'text': scene['text']
        })

    # 3. Create Video
    editor = VideoEditor()
    output_file = "output/final_video.mp4"
    logger.info("Rendering video...")
    success = editor.create_video(processed_scenes, output_file)
    
    if success:
        logger.info(f"Video generated successfully: {output_file}")
    else:
        logger.error("Video generation failed")

    if not args.dry_run and success:
        # Upload legic here
        logger.info("Uploading to YouTube... (TODO)")

if __name__ == "__main__":
    asyncio.run(main())

