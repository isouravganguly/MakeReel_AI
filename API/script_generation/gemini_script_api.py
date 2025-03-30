import json
from typing import List, Optional
from pydantic import BaseModel
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, SCRIPT_ENABLED

# ------------------------------
# Define Pydantic Models
# ------------------------------

class Paragraph(BaseModel):
    text: str
    image_desc: str
    image_path: Optional[str] = None
    voice_path: Optional[str] = None

class ScriptOutput(BaseModel):
    script: str
    paragraphs: List[Paragraph]
    bg_track: str

# ------------------------------
# GeminiFlashScriptGenerator Class
# ------------------------------

class GeminiFlashScriptGenerator:
    def __init__(self, api_key: str = GEMINI_API_KEY, enabled: bool = SCRIPT_ENABLED):
        """
        Initialize the generator using configuration from the global config.
        If generation is disabled, returns mock data.
        """
        self.api_key = api_key
        self.enabled = enabled
        # Create the client only if generation is enabled.
        self.client = genai.Client(api_key=self.api_key) if self.enabled else None
        self.model = "gemini-2.0-flash"

    def generate_script(self, theme: str) -> ScriptOutput:
        """
        Generates a creative video script using Gemini Flash.
        Returns a ScriptOutput object containing:
          - script: overall script text,
          - paragraphs: list of Paragraph objects (each with narrative text and image description),
          - bg_track: background music track description.
        In case of errors or if generation is disabled, returns a fallback ScriptOutput.
        """
        if not self.enabled:
            print("Script generation disabled, returning mock data.")
            return ScriptOutput(
                script="[MOCK] Sample script",
                paragraphs=[
                    Paragraph(
                        text="Sample paragraph",
                        image_desc="Sample image description"
                    )
                ],
                bg_track="epic cinematic"
            )
        
        # Construct the prompt with instructions to return valid JSON.
        prompt = (
    f"Generate a creative video script for a Brand on the theme '{theme}'. You are a marketing company, and this is a promotional video. The final output should be a 20-second reel divided into 4 short paragraphs (about 5 seconds each). "
    "For each paragraph, provide:\n"
    "1. A brief narrative that sounds natural and human—with realistic pauses, filler words, slight repetitions, and natural punctuation (e.g., commas, ellipses) to indicate breathing and pauses. For example: 'Movies, oh my gosh, I just just absolutely love them... They're like time machines taking you to different worlds, and um, I just can't get enough of it.'\n"
    "2. A one-sentence, concise image description that visually represents the narrative of that paragraph.\n"
    "Also, provide an overall short description for a background music track that sets an appropriate mood for the reel.\n"
    "Ensure that the script text conveys a natural, human-like cadence and includes small errors or hesitations to enhance realism.\n"
    "Return the result as valid JSON with the following keys:\n"
    "  - 'script': a summary or title of the entire reel,\n"
    "  - 'paragraphs': an array of objects, each containing 'text' (the paragraph narrative) and 'image_desc' (the image description), and\n"
    "  - 'bg_track': a brief description of the background music track."
)

            # prompt = (
            #     f"Generate a creative, engaging video script for a brand on the theme '{theme}'. You are a top-tier marketing agency tasked with producing a compelling 20-second promotional reel. The reel should be divided into 4 distinct 5-second paragraphs. Each paragraph must feature a natural, conversational narrative with realistic pauses, subtle filler words, and slight hesitations that mimic human speech, while incorporating persuasive hooks, clear calls-to-action, and emotionally resonant language. Use proper punctuation—including commas, ellipses, and dashes—to accurately reflect a human cadence.\n\n"
            #     "For each paragraph, provide:\n"
            #     "1. A brief, authentic narrative that sounds human and natural, capturing the brand’s essence and engaging the audience with relatable language and marketing hooks. For example: 'Imagine a moment—so genuine, so unforgettable—where every detail sparks your curiosity, and you just have to act.'\n"
            #     "2. A one-sentence, concise image description that visually represents the narrative and reinforces the brand message.\n\n"
            #     "Additionally, provide a short description for a background music track that sets the perfect mood for the reel, enhancing its energy and appeal.\n\n"
            #     "Return the result as valid JSON with the following keys:\n"
            #     "  - 'script': a summary or title for the overall reel,\n"
            #     "  - 'paragraphs': an array of objects, each containing 'text' (the narrative) and 'image_desc' (the image description), and\n"
            #     "  - 'bg_track': a brief description of the background music track."
            # )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=600,  # Increased token limit to reduce truncation risk
                    temperature=0.7,
                    response_mime_type="application/json",
                    response_schema=ScriptOutput  # Use our Pydantic model as the expected schema
                )
            )
            print("Response received from Gemini Flash API.")
            
            # If the SDK automatically parsed the response, use it.
            if response.parsed:
                return response.parsed

            # Otherwise, manually parse the raw text.
            raw_text = response.text.strip()
            # Remove markdown code fences if present.
            if raw_text.startswith("```json"):
                start_index = raw_text.find("{")
                end_index = raw_text.rfind("}") + 1
                json_text = raw_text[start_index:end_index]
            else:
                json_text = raw_text

            parsed_output = ScriptOutput.parse_raw(json_text)
            return parsed_output
        except Exception as e:
            print("Error generating script:", e)
            # Return fallback output in case of errors.
            return ScriptOutput(
                script="Failed to generate script.",
                paragraphs=[],
                bg_track=""
            )

# ------------------------------
# Test the Implementation (for standalone testing)
# ------------------------------

if __name__ == "__main__":
    generator = GeminiFlashScriptGenerator()
    theme = "Nature Adventure"
    script_output = generator.generate_script(theme)
    print("Generated Script Output:")
    print(script_output.json(indent=2))
