import time
import json
import google.generativeai as genai
from .config import Config

class LLMWrapper:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def _call_gemini(self, prompt, max_retries=5):
        """Helper to call Gemini with exponential backoff for 429s."""
        for i in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                # Check if it's a rate limit error (429)
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    wait_time = (2 ** i) + 5 # 5, 7, 9, 13, 21 seconds...
                    print(f"Rate limited (429). Waiting {wait_time}s before retry {i+1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Gemini API Error: {e}")
                    raise e
        return None

    def generate_psychology_titles(self):
        """Generates 20 viral psychology titles."""
        prompt = """
        You are a high-level YouTube title strategist known for creating viral psychology-based content. Your niche focuses on deep archetypes, childhood trauma, emotional neglect, and hidden social dynamics.
        Objective: Write exactly 20 highly clickable, emotionally intense YouTube titles.
        
        Mandatory Rules:
        For Angle 1 & Angle 2, every title must begin with: “The Psychology of…” or “The Hidden Pain of…”
        Naturally include powerful psychological keywords such as: PSYCHOLOGY, CHILDHOOD, TRAUMA, QUIET, ANXIOUS, LONELY, HIDDEN, PAIN, NEGLECTED, SILENT, SELF-SABOTAGE
        Highlight 1–2 words in ALL CAPS for emotional impact
        Add emotional hook tags like: [The Dark Truth], [Life Changing], [Must Watch], [Warning]
        Each title must be under 80 characters
        
        Content Structure (Strictly Follow):
        Angle 1: Childhood Wounds & Upbringing – 5 Titles ("The Psychology of a Child Who...", "The Lifelong Effect of...")
        Angle 2: Adult Traits & Social Archetypes – 10 Titles ("The Psychology of People Who...", "Why [Trait] Suffer the Most")
        Angle 3: Dark Psychology & Power Dynamics – 5 Titles ("The 3 Laws of...", "NEVER Show...", "The Dark Rule of...")
        
        STRICT OUTPUT FORMAT:
        Return ONLY Valid JSON. A simple list of strings.
        ["Title 1", "Title 2", ...]
        """
        try:
            text = self._call_gemini(prompt)
            if not text: return []
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error generating titles: {e}")
            return []

    def generate_psychology_script(self, title):
        """Generates a long-form psychology script."""
        prompt = f"""
        You are a Viral Content Writer specializing in long-form, emotionally immersive psychological and philosophical video essays.
        
        Title: {title}
        
        MANDATORY STRATEGIC DEDUCTION STEP:
        Identify the Core Archetype Angle implied in the title. This must act as the emotional spine.
        
        SCRIPT GENERATION INSTRUCTIONS:
        1. Hook & Core Paradox (2-3 min): Speak directly to viewer ("You"), reveal core paradox.
        2. Definition & Psychological Authority (3-4 min): Define concepts (Parentification, Hypervigilance, etc), show effect on nervous system.
        3. Emotional Cost & Philosophical Weight (3-4 min): Loss of authenticity, reference Jung/Seneca/Rilke.
        4. Adult Patterns & Unlearning (4-5 min): Connect childhood to adult behavior (relationships, career).
        5. Healing & Closing (3-4 min): Practical tools (Inner Child, Shadow Work), strong quote.
        
        STRICT OUTPUT FORMAT:
        Return ONLY Valid JSON.
        {{
            "title": "{title}",
            "deduced_angle": "The deduced angle...",
            "scenes": [
                {{
                    "section": "Hook",
                    "text": "The spoken narration for this part...",
                    "visual_keyword": "A single precise keyword for Pexels search (e.g. 'Lonely Child', 'Stormy Sea')",
                    "visual_prompt": "An oil painting of... (detailed prompt for AI image gen)"
                }},
                ...
            ]
        }}
        Create enough scenes to cover 12-20 minutes of narration (approx 1800-3000 words).
        """
        try:
            text = self._call_gemini(prompt)
            if not text: return None
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error generating script: {e}")
            return None

    def generate_psychology_short_script(self, title):
        """Generates a 60-second viral psychology short script."""
        prompt = f"""
        You are a generic YouTube Shorts strategist specializing in dark, viral psychology.
        Title: {title}
        
        Objective: Create a high-retention, loopable 60-second Short script (approx 150-180 words).
        Tone: Direct, Intimate, Authoritative, "The Hidden Pain".
        
        Structure:
        1. The Hook (0-5s): Stop the scroll. "You might be..." or "If you..."
        2. The Reveal (5-20s): Explain the hidden psychological mechanism.
        3. The Cost (20-40s): Why this hurts/ruins relationships.
        4. The Fix/Closing (40-60s): One powerful sentence of advice.
        
        STRICT OUTPUT FORMAT:
        Return ONLY Valid JSON.
        {{
            "title": "{title}",
            "scenes": [
                {{
                    "text": "Spoken text...",
                    "visual_keyword": "Visual keyword for Pexels (portrait)",
                    "visual_prompt": "Oil painting style prompt..."
                }},
                ...
            ]
        }}
        """
        try:
            text = self._call_gemini(prompt)
            if not text: return None
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error generating short script: {e}")
            return None
