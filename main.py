from API.image_generation import gemini_image_api
from API.script_generation import gemini_script_api
from API.voice_generation import google_tts_generator
from API.video_editor_service import create_paragraph_clip
from API.mock_data.generate_mock_script_output import generate_mock_script_output
from config import SYSTEM_DOWNTIME

def build_video_assets(theme: str):
    # If the system is in downtime mode, use mock data.
    print("System downtime mode:", SYSTEM_DOWNTIME)
    if SYSTEM_DOWNTIME:
        print("System is in downtime mode, using mock data.")
        script_data = generate_mock_script_output()
        print("Mock data generated successfully!", script_data)
        final_video_file = create_paragraph_clip.stitch_video(script_data, transition_duration=0.5)
    else:
        # Initialize the services.
        script_generator = gemini_script_api.GeminiFlashScriptGenerator()
        image_generator = gemini_image_api.GeminiFlashImageGenerator()
        tts_generator = google_tts_generator.GoogleTTSGenerator()
        
        # 1. Generate the script using Gemini.
        script_data = script_generator.generate_script(theme)
        
        # 2. For each paragraph, generate an image and a voice file.
        for para in script_data.paragraphs:
            para.image_path = image_generator.generate_image(para.image_desc)
            para.voice_path = tts_generator.generate_voice(para.text)
        
        print("Script, Images, and Voice generated successfully!", script_data)
        
        # 3. Stitch all the paragraph clips into one final video.
        final_video_file = create_paragraph_clip.stitch_video(script_data, transition_duration=0.5)
    
    return {
        "script_data": script_data,
        "final_video": final_video_file
    }

if __name__ == "__main__":
    theme = "I am a Physician, My name is Saoumo-deep Roy. My brother, AORKO and sister-in-law, Chaayaanikaa are amazing Dentists. We have an amazing family and Clinic, called the ROY CLINICS, situated in Dhaanbaad. Now you know where to reach out for you needs."
    assets = build_video_assets(theme)
    print("Generated Assets:")
    print(assets)
