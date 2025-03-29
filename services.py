# services.py

import requests
import json
from google import genai
from google.genai import types

class GeminiFlashScriptGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"

    def generate_script(self, theme: str) -> dict:
        """
        Generates a creative video script using Gemini Flash.
        The prompt instructs the model to create:
         - A full script text,
         - Paragraphs with narrative text and a concise image description for each,
         - An overall background track description.
        The output should be formatted as JSON with keys:
         - "script": full text,
         - "paragraphs": list of objects, each with "text" and "image_desc",
         - "bg_track": background music track description.
        """
        prompt = (
            f"Generate a creative video script for a brand based on the theme: '{theme}'.\n"
            "Divide the script into several paragraphs. For each paragraph, include:\n"
            "1. The narrative text.\n"
            "2. A concise description for an image that fits the narrative.\n"
            "Also, provide an overall description for a background music track.\n"
            "Format the output as valid JSON with the keys: 'script', 'paragraphs' (list of objects with 'text' and 'image_desc'), and 'bg_track'."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=500,
                    temperature=0.7
                )
            )
            output_text = response.text.strip()
            # Attempt to parse the output as JSON.
            parsed_output = json.loads(output_text)
            return parsed_output
        except Exception as e:
            print("Error generating script:", e)
            return {
                "script": "Failed to generate script.",
                "paragraphs": [],
                "bg_track": ""
            }

def generate_image(self, description: str) -> str:
        """
        Generate an image based on the provided description using Hugging Face’s Inference API.
        Returns the file path to the generated image.
        """
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": description}

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            # The API returns image data; save it to a file.
            safe_desc = "".join([c if c.isalnum() else "_" for c in description[:10]])
            image_path = f"generated_{safe_desc}.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"Image generated and saved as {image_path}")
            return image_path
        else:
            print("Image generation failed:", response.text)
            return None

def generate_voice_over(self, text: str, voice_type: str, gender: str, background_music: bool = False) -> str:
        """
        Generate a voice over audio file for the given text using ElevenLabs.
        Returns the file path to the generated audio file.
        """
        # ElevenLabs endpoint URL; ensure you replace YOUR_VOICE_ID with a valid voice id.
        api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            # Voice settings can be adjusted based on your needs.
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