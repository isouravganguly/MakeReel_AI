from typing import Optional, List
from pydantic import BaseModel
from google import genai
from google.genai import types

class Paragraph(BaseModel):
    text: str
    image_desc: str
    image_path: Optional[str] = None

class ScriptOutput(BaseModel):
    script: str
    paragraphs: List[Paragraph]
    bg_track: str

class GeminiFlashScriptGenerator:
    def __init__(self, api_key: str, enabled: bool = True):
        self.api_key = api_key
        self.enabled = enabled
        self.client = genai.Client(api_key=self.api_key) if enabled else None
        self.model = "gemini-2.0-flash"

    def generate_script(self, theme: str) -> ScriptOutput:  # This line was not indented
        if not self.enabled:
            print("Script generation disabled, returning mock data")
            return ScriptOutput(
                script="[MOCK] Sample script",
                paragraphs=[Paragraph(
                    text="Sample paragraph", 
                    image_desc="Sample image description"
                )],
                bg_track="epic cinematic"
            )
        """
        Generates a creative video script using Gemini Flash with JSON output.
        """
        prompt = (
            f"Generate a creative video script for a brand based on the theme: '{theme}'.\n"
            "Divide the script into several paragraphs. For each paragraph, include:\n"
            "1. The narrative text.\n"
            "2. A concise description for an image that fits the narrative.\n"
            "Also, provide an overall description for a background music track.\n"
            "Return the result as valid JSON."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=600,  # increased token limit
                    temperature=0.7,
                    response_mime_type="application/json",
                    response_schema=ScriptOutput
                )
            )
            print("Response:", response)

            # Attempt to use the parsed output provided by the SDK.
            if response.parsed:
                return response.parsed

            # Otherwise, get the raw text.
            raw_text = response.text.strip()

            # If the output is wrapped in markdown fences, remove them.
            if raw_text.startswith("```json"):
                start_index = raw_text.find("{")
                end_index = raw_text.rfind("}") + 1
                json_text = raw_text[start_index:end_index]
            else:
                json_text = raw_text

            # Try parsing the JSON text.
            parsed_output = ScriptOutput.parse_raw(json_text)
            return parsed_output
        except Exception as e:
            print("Error generating script:", e)
            # Optionally, log the raw output for debugging:
            # print("Raw output:", raw_text)
            return ScriptOutput(script="Failed to generate script.", paragraphs=[], bg_track="")