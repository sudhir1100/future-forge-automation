# Voice Cloning for YouTube - Complete GitHub Setup

## 🎯 Overview
A lightweight, free voice cloning solution using open-source models. No API costs, unlimited usage.

## 📦 Repository Structure
```
voice-cloning-youtube/
├── app.py                 # Flask API server
├── clone_voice.py         # Voice cloning script
├── requirements.txt       # Python dependencies
├── samples/              # Store your voice sample here
│   └── my_voice.wav
├── scripts/              # Your video scripts
│   ├── short_1.txt
│   └── long_1.txt
├── output/               # Generated voiceovers
└── README.md
```

## 🚀 Quick Start

### 1. Setup
```bash
pip install -r requirements.txt
```

### 2. Add Your Voice Sample
- Record 10-30 seconds of your voice speaking clearly
- Save as `samples/my_voice.wav`

### 3. Generate Voiceover
```bash
python clone_voice.py --sample samples/my_voice.wav --script scripts/short_1.txt --output output/short_1.mp3
```

---

## 📄 API Usage (Flask)
Run the server:
```bash
python app.py
```
Send a request:
```bash
POST http://localhost:5000/generate
{
    "script": "Hello world"
}
```

---

## 🎬 Batch Processing
```bash
bash batch_generate.sh
```

---

## 🐳 Docker Deployment
```bash
docker-compose up -d
```

---

## 📊 System Requirements
- **RAM**: 8GB Minimum (16GB Recommended)
- **GPU**: NVIDIA GPU with 4GB+ VRAM (Optional, but 10x faster)

