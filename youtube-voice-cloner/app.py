#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
from TTS.api import TTS
import os
import uuid
import torch

app = Flask(__name__)

# Auto-detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"--- API using device: {device.upper()} ---")

# Initialize TTS model globally
print("🎤 Initializing XTTS v2 model for API...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

SAMPLE_PATH = "samples/my_voice.wav"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_voiceover():
    """
    API endpoint to generate voiceover
    
    POST body:
    {
        "script": "Your text here",
        "sample": "samples/custom_sample.wav" (Optional)
    }
    """
    data = request.json
    script = data.get('script', '')
    sample = data.get('sample', SAMPLE_PATH)
    
    if not script:
        return jsonify({"error": "No script provided"}), 400
    
    if not os.path.exists(sample):
        return jsonify({"error": f"Voice sample not found: {sample}"}), 404
    
    # Generate unique filename
    output_file = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp3")
    
    try:
        tts.tts_to_file(
            text=script,
            speaker_wav=sample,
            language="en",
            file_path=output_file
        )
        
        return send_file(output_file, mimetype="audio/mpeg")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "device": device})

if __name__ == '__main__':
    # Using threaded=False because TTS model might not be thread-safe on some devices
    app.run(host='0.0.0.0', port=5000, threaded=False)
