
import os
import sys
import argparse
import torch
from TTS.api import TTS

def clone_voice(sample_path, script_text, output_path):
    """
    Clone voice and generate speech from script
    """
    # Auto-detect device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"--- Using device: {device.upper()} ---")

    print("🎤 Initializing XTTS v2 model...")
    try:
        # Initialize XTTS v2
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)
    
    print(f"🔊 Cloning voice from: {sample_path}")
    print(f"📝 Script length: {len(script_text)} characters")
    
    try:
        # Generate speech with cloned voice
        tts.tts_to_file(
            text=script_text,
            speaker_wav=sample_path,
            language="en",
            file_path=output_path
        )
        print(f"✅ Voiceover saved to: {output_path}")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Clone voice and generate voiceovers")
    parser.add_argument("--sample", required=True, help="Path to voice sample file")
    parser.add_argument("--script", required=True, help="Path to script text file")
    parser.add_argument("--output", required=True, help="Path to output audio file")
    
    args = parser.parse_args()
    
    # Read script
    if not os.path.exists(args.script):
        print(f"❌ Script file not found: {args.script}")
        sys.exit(1)
    
    with open(args.script, 'r', encoding='utf-8') as f:
        script_text = f.read().strip()
    
    # Check sample exists
    if not os.path.exists(args.sample):
        print(f"❌ Voice sample not found: {args.sample}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    
    # Generate voiceover
    clone_voice(args.sample, script_text, args.output)

if __name__ == "__main__":
    main()

