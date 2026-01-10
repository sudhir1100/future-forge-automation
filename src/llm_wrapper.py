import json
import google.generativeai as genai
from .config import Config

class LLMWrapper:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_script(self, topic):
        """
        Generates a YouTube script for the given topic.
        Returns a JSON object with: title, script (list of sentences), keywords (per sentence)
        """
        prompt = f"""
        Act as a professional YouTube scriptwriter for a Tech & AI channel.
        Topic: {topic}
        
        Create a high-energy, engaging 60-second Short script.
        
        STRICT OUTPUT FORMAT:
        You must return ONLY Valid JSON. No markdown formatting, no code blocks (```json).
        
        JSON Structure:
        {{
            "title": "Viral Title",
            "description": "SEO optimized description with hashtags",
            "scenes": [
                {{
                    "text": "Spoken text for this segment (keep it punchy).",
                    "visual_keyword": "A single precise keyword for stock footage search (e.g. 'Cyberpunk City', 'Robot Hand', 'Circuit Board')"
                }}
            ]
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            # clean response if it contains markdown code blocks
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error generating script: {e}")
            return None
