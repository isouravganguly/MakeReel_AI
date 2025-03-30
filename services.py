# services.py

import requests
import json
from typing import Optional, List
from pydantic import BaseModel
from google import genai
from google.genai import types
import time
import re
import base64

class Paragraph(BaseModel):
    text: str
    image_desc: str
    image_path: Optional[str] = None

class ScriptOutput(BaseModel):
    script: str
    paragraphs: List[Paragraph]
    bg_track: str

class GeminiFlashScriptGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"

    def generate_script(self, theme: str) -> ScriptOutput:
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

class ImageGenerationService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"

    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024, steps: int = 4, seed: int = 0, output_format: str = "jpeg", response_format: str = "b64") -> str:
        """
        Generate an image using getimg.ai's text-to-image API.
        The image is returned as Base64 data. This function decodes that data,
        saves it to a file, and returns the file path.
        """
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "seed": seed,
            "output_format": output_format,
            "response_format": response_format
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Error during API call:", e)
            return None

        # Expecting a JSON response with an "image" field containing Base64 data.
        data = response.json()
        image_b64 = data.get("image")
        if not image_b64:
            print("Image generation failed: No 'image' field in response:", data)
            return None

        try:
            image_data = base64.b64decode(image_b64)
        except Exception as e:
            print("Error decoding base64 image data:", e)
            return None

        # Generate a safe, unique filename.
        safe_prompt = re.sub(r'[^A-Za-z0-9]', '_', prompt[:10])
        timestamp = int(time.time())
        file_name = f"getimg_{safe_prompt}_{timestamp}.{output_format}"

        try:
            with open(file_name, "wb") as f:
                f.write(image_data)
            print(f"Image generated and saved as {file_name}")
            return file_name
        except Exception as e:
            print("Error saving image:", e)
            return None

class VoiceOverService:
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id

    def generate_voice_over(self, text: str, voice_type: str, gender: str, background_music: bool = False) -> str:
        """
        Generate a voice over audio file for the given text using ElevenLabs.
        Returns the file path to the generated audio file.
        """
        api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            audio_path = "voice_over.mp3"
            with open(audio_path, "wb") as f:
                f.write(response.content)
            print(f"Voice over generated and saved as {audio_path}")
            return audio_path
        else:
            print("Voice over generation failed:", response.text)
            return None
