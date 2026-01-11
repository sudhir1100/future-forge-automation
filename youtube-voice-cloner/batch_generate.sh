#!/bin/bash

# Configuration
SAMPLE="samples/my_voice.wav"
OUTPUT_DIR="output"
SCRIPT_DIR="scripts"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🚀 Starting batch generation..."

for script in "$SCRIPT_DIR"/*.txt; do
    if [ -f "$script" ]; then
        filename=$(basename "$script" .txt)
        echo "🔊 Processing: $filename"
        
        python clone_voice.py \
          --sample "$SAMPLE" \
          --script "$script" \
          --output "$OUTPUT_DIR/${filename}.mp3"
        
        if [ $? -eq 0 ]; then
            echo "✅ Done: ${filename}.mp3"
        else
            echo "❌ Failed: $filename"
        fi
    fi
done

echo "✨ Batch generation complete!"
