# Future Forge - Automated AI YouTube Channel

A fully automated YouTube content generation engine targeting the "Future Tech & AI" niche.

## Tech Stack
- **Engine**: Python 3.10+
- **Brain**: Google Gemini API
- **Voice**: Edge TTS (Microsoft Azure Neural Voices)
- **Visuals**: Pexels API
- **Editing**: FFmpeg + MoviePy
- **Hosting**: GitHub Actions (Cron Schedule)

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_key_here
   PEXELS_API_KEY=your_key_here
   ```

3. **Usage**
   ```bash
   python src/main.py --dry-run
   ```
