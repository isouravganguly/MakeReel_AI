import requests
import time
import re
import base64

class ImageGenerationService:
    def __init__(self, api_key: str, enabled: bool = True):
        self.api_key = api_key
        self.enabled = enabled
        self.url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"

    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024, 
                      steps: int = 4, seed: int = 0, output_format: str = "jpeg", 
                      response_format: str = "b64") -> str:
        if not self.enabled:
            print("Image generation disabled, returning mock path")
            return f"mock_image_{prompt[:10]}.jpg"
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
        print("Image generation payload:", payload)
        print("Image generation API key:", self.api_key)
        print("Image generation URL:", self.url)

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