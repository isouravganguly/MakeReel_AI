# main.py

from services import GeminiFlashScriptGenerator, ImageGenerationService, VoiceOverService

def build_video_assets(theme: str,
                       gemini_api_key: str,
                       hf_token: str,
                       elevenlabs_api_key: str,
                       voice_id: str,
                       voice_type: str = "DeepVoice",
                       gender: str = "Male",
                       background_music: bool = False):
    # Initialize the service wrappers with your API keys.
    gemini_generator = GeminiFlashScriptGenerator(api_key=gemini_api_key)
    image_service = ImageGenerationService(hf_token=hf_token)
    voice_service = VoiceOverService(api_key=elevenlabs_api_key, voice_id=voice_id)
    
    # 1. Generate the script with image descriptions and background track details.
    script_data = gemini_generator.generate_script(theme)
    print("Generated Script Data:")
    print(script_data)
    
    # 2. Generate images for each paragraph.
    for idx, para in enumerate(script_data["paragraphs"]):
        image_desc = para["image_desc"]
        image_path = image_service.generate_image(image_desc)
        script_data["paragraphs"][idx]["image_path"] = image_path
    
    # 3. Generate the voice over for the entire script text.
    voice_over_path = voice_service.generate_voice_over(
        text=script_data["script"],
        voice_type=voice_type,
        gender=gender,
        background_music=background_music
    )
    
    # Bundle all assets.
    assets = {
        "script_data": script_data,
        "voice_over": voice_over_path
    }
    
    return assets

if __name__ == "__main__":
    theme = "Nature Adventure"
    gemini_api_key = "YOUR_GEMINI_API_KEY"
    hf_token = "YOUR_HF_TOKEN"
    elevenlabs_api_key = "YOUR_ELEVENLABS_API_KEY"
    voice_id = "YOUR_VOICE_ID"
    
    assets = build_video_assets(
        theme, 
        gemini_api_key=gemini_api_key, 
        hf_token=hf_token, 
        elevenlabs_api_key=elevenlabs_api_key, 
        voice_id=voice_id, 
        voice_type="DeepVoice", 
        gender="Male", 
        background_music=False
    )
    print("Generated Assets:")
    print(assets)
