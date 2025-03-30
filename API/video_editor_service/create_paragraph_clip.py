from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy import vfx, afx
import os
import time
from API.script_generation import gemini_script_api
from API.image_generation import gemini_image_api
from API.voice_generation import google_tts_generator
import mutagen

def create_paragraph_clip(paragraph, transition_duration=0.5):
    """
    Creates a video clip for a single paragraph.
    The clip duration is determined by the duration of the voice-over audio file.
    If no image is provided, a bright solid background with overlay text is used.
    Fade-in and fade-out transitions can be applied for smooth merging.
    """
    # Load the audio clip and determine its duration.
    print("Processing audio file:", paragraph.voice_path)
    audio_clip = AudioFileClip(paragraph.voice_path)
    duration = audio_clip.duration
    print("Audio duration (seconds):", duration)
    
    # Check if the image path is available.
    if paragraph.image_path:
        # Create an image clip from the provided image file.
        background_clip = ImageClip(paragraph.image_path).with_duration(duration).with_effects([vfx.Resize((1280, 720))])
    else:
         # No image provided: use a bright solid background (e.g., bright yellow).
        background_clip = ColorClip(size=(1280, 720), color=(255, 255, 0), duration=duration)
        # Define the path to your OpenType font file.
        # Updated font path handling
        font_path = os.path.join(
            os.path.dirname(__file__), 
            "../../assets/fonts/Poppins-SemiBold.ttf"
        )
        
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found at: {font_path}. Please install the Poppins font or use a system font.")
        
        # Alternative system font (uncomment if needed)
        # font_path = "Arial"  # Use system font as fallback
        # Create a TextClip with the paragraph text.
        text_overlay = TextClip(
            font=font_path,
            text=paragraph.text,
            font_size=40,
            color="#000000",       # Black text color.
            bg_color="#FFFFFF",     # White background for text.
            method="caption",
            size=(1200, None),
            duration=duration
        ).with_position("center")
        # Composite the text overlay over the solid background.
        background_clip = CompositeVideoClip([background_clip, text_overlay])
    
    # Attach the audio to the clip.
    video_clip = background_clip.with_audio(audio_clip)
    print("Video clip created successfully! Duration:", video_clip.duration)
    
    # Optionally apply fade-in and fade-out transitions.
    # Uncomment the next line to enable transitions:
    # video_clip = video_clip.fx(vfx.fadein, duration=transition_duration).fx(vfx.fadeout, duration=transition_duration)
    
    return video_clip

def stitch_video(script_data, transition_duration=0.5, final_filename="final_video.mp4"):
    """
    Iterates through the paragraphs in script_data, creates a video clip for each segment 
    (with duration based on the voice-over length and transition effects), and stitches them 
    into one final MP4 video.
    
    Returns:
      The file path to the final video.
    """
    clips = []
    for para in script_data.paragraphs:
        clip = create_paragraph_clip(para, transition_duration)
        clips.append(clip)
        print("Clip added with duration:", clip.duration)
    
    # Concatenate all clips.
    # If you wish to have crossfade transitions between clips, you can set the transition parameter.
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the final video file.
    final_clip.write_videofile(final_filename, fps=24)
    
    return final_filename
