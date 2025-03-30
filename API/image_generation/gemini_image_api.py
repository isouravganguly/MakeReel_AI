import os
import time
import re
from io import BytesIO
from typing import Optional
from PIL import Image
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, IMAGE_ENABLED  # Import global config values

class GeminiFlashImageGenerator:
    def __init__(self, api_key: str = GEMINI_API_KEY, enabled: bool = IMAGE_ENABLED):
        """
        Initialize the Gemini Flash Image Generator using configuration values.
        If generation is disabled, the generator will return a mock image file name.
        """
        self.api_key = api_key
        self.enabled = enabled
        self.client = genai.Client(api_key=self.api_key) if self.enabled else None
        self.model = "gemini-2.0-flash-exp-image-generation"

    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generates an image using the Gemini API based on the provided prompt.
        Sends the prompt to the model and expects inline image data in the response.
        The image is decoded, saved locally, and the file path is returned.
        
        If image generation is disabled, returns a mock image file name.
        """
        if not self.enabled:
            print("Image generation disabled, returning mock path.")
            return "gemini_image_A_group_of_1743261835.png"

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
        except Exception as e:
            print("Error during API call:", e)
            return None

        # Check if the response has candidates and valid content
        if not response or not response.candidates or len(response.candidates) == 0:
            print("No candidates returned in the response.")
            return None

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            print("No content parts found in the candidate.")
            return None

        image_file = None
        # Iterate through candidate parts to find inline image data.
        for part in candidate.content.parts:
            if part.inline_data is not None:
                try:
                    # Convert inline binary data to an image using Pillow.
                    image = Image.open(BytesIO(part.inline_data.data))
                    # Generate a safe and unique filename.
                    safe_prompt = re.sub(r'[^A-Za-z0-9]', '_', prompt[:10])
                    timestamp = int(time.time())
                    file_name = f"gemini_image_{safe_prompt}_{timestamp}.png"
                    image.save(file_name)
                    print(f"Image generated and saved as {file_name}")
                    image_file = file_name
                    break
                except Exception as e:
                    print("Error processing image data:", e)
        if not image_file:
            print("No image data found in the response.")
        return image_file

# Example usage (for testing purposes):
if __name__ == "__main__":
    prompt = ("Create a 3D rendered image of a pig with wings and a top hat "
              "flying over a futuristic sci-fi city with lots of greenery.")
    image_generator = GeminiFlashImageGenerator()
    file_path = image_generator.generate_image(prompt)
    print("Generated image file:", file_path)
