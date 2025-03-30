from google.cloud import texttospeech
import os
import time
import re
from config import VOICE_ENABLED

class GoogleTTSGenerator:
    def __init__(self, enabled: bool = VOICE_ENABLED):
        """
        Initializes the Text-to-Speech client using ADC.
        Ensure that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        """
        self.enabled = enabled
        if self.enabled:
            self.client = texttospeech.TextToSpeechClient()
        else:
            self.client = None

    def _generate_safe_filename(self, text: str, extension: str) -> str:
        """
        Generates a safe, unique filename based on the first 10 characters of the text and a timestamp.
        """
        safe_text = "".join(c if c.isalnum() else "_" for c in text[:10])
        timestamp = int(time.time())
        return f"voice_{safe_text}_{timestamp}.{extension}"

    def generate_voice(self, text: str, language_code: str = "en-US",
                       ssml_gender: str = "MALE",
                       voice_name: str = "en-US-Chirp-HD-D",   # Specify a particular voice if desired
                       audio_encoding: str = "MP3",
                       speaking_rate: float = 1.0,
                       pitch: float = 0.0,
                       volume_gain_db: float = 0.0,
                       effects_profile_ids: list = None,
                       output_file: str = None) -> str:
        """
        Converts input text to speech.
        
        Parameters:
          - text: The text to be synthesized.
          - language_code: e.g., "en-US".
          - ssml_gender: "NEUTRAL", "MALE", or "FEMALE".
          - voice_name: Specific voice variant name (optional).
          - audio_encoding: e.g., "MP3" or "LINEAR16".
          - speaking_rate: Speech speed (default is 1.0; lower is slower, higher is faster).
          - pitch: Pitch adjustment in semitones (default is 0.0).
          - volume_gain_db: Volume adjustment in dB (default is 0.0).
          - effects_profile_ids: List of effects profile IDs (e.g., ["handset-class-device"]).
          - output_file: Name of the file to save the synthesized audio. If not provided, one is generated.
        
        Returns:
          The path to the generated audio file.
        """
        # If generation is disabled, return a mock file name.
        if not self.enabled:
            print("Voice generation disabled, returning mock file.")
            return "mock_voice_over.mp3"

        # If output_file is not provided, generate one safely.
        if not output_file:
            output_file = self._generate_safe_filename(text, "mp3")

        # Set the text input.
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice selection request.
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL),
            name=voice_name
        )

        # Build the audio configuration with additional parameters.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding.upper(), texttospeech.AudioEncoding.MP3),
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume_gain_db=volume_gain_db,
            effects_profile_id=effects_profile_ids if effects_profile_ids else []
        )

        # Perform the text-to-speech request.
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Write the response audio content to a file.
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file '{output_file}'")
        return output_file

# Example usage:
if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to the path of your service account JSON.
    tts = GoogleTTSGenerator()
    sample_text = "Hello world! This is a sample text-to-speech conversion using Google Cloud TTS."
    output_path = tts.generate_voice(
        sample_text,
        language_code="en-US",
        ssml_gender="NEUTRAL",
        voice_name="en-US-Chirp-HD-D",
        speaking_rate=0.50,  # Slightly slower for a more natural delivery
        pitch=-2.0,          # Slightly lower pitch
        volume_gain_db=2.0,    # Slight volume boost
        effects_profile_ids=["handset-class-device"]
    )
    print("Generated audio file:", output_path)
