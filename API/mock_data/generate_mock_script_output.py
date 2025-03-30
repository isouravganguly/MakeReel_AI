from API.script_generation.gemini_script_api import Paragraph, ScriptOutput
import time

def generate_mock_script_output():
    # Generate 12 paragraphs (each ~5 seconds) for a 1-minute content.
    paragraphs = []
    for i in range(1, 8):
        # Create some mock text that includes natural pauses and filler words.
        text = (f"Paragraph {i}: Okay, so, imagine this... you're, like, in the midst of a "
                f"coding adventure, where every keystroke reveals a new secret. It's, um, pretty "
                f"exciting, right?")
        # Create a corresponding image description.
        image_desc = (f"Image {i} description: A vibrant scene depicting digital landscapes with "
                      f"pixelated elements and dynamic colors, illustrating the coding adventure.")
        # For mock purposes, use fixed file names (in practice these would be generated dynamically)
        image_path = None
        voice_path = f"mock_voice_{i}.mp3"
        
        para = Paragraph(
            text=text,
            image_desc=image_desc,
            image_path=image_path,
            voice_path=voice_path
        )
        paragraphs.append(para)
    
    # Create an overall script summary/title and a background track description.
    script_title = "Coding Adventure in Pixels"
    bg_track = ("Upbeat, chiptune-inspired music with a playful and adventurous feel. "
                "Starts softly and builds in intensity as the journey progresses.")
    
    # Create and return the ScriptOutput object.
    return ScriptOutput(
        script=script_title,
        paragraphs=paragraphs,
        bg_track=bg_track
    )

# Example usage:
if __name__ == "__main__":
    mock_script = generate_mock_script_output()
    # For display purposes, you can convert it to JSON:
    print(mock_script.json(indent=2))
