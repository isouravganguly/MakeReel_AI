from google.cloud import texttospeech
import os

class GoogleTTSGenerator:
    def __init__(self):
        """
        Initializes the Text-to-Speech client using ADC.
        Ensure that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        """
        self.client = texttospeech.TextToSpeechClient()

    def generate_voice(self, text: str, language_code: str = "en-US",
                       ssml_gender: str = "NEUTRAL",
                       audio_encoding: str = "MP3",
                       output_file: str = "output.mp3") -> str:
        """
        Converts input text to speech.
        
        Parameters:
          - text: The text to be synthesized.
          - language_code: e.g., "en-US".
          - ssml_gender: "NEUTRAL", "MALE", or "FEMALE".
          - audio_encoding: e.g., "MP3" or "LINEAR16".
          - output_file: Name of the file to save the synthesized audio.
        
        Returns:
          The path to the generated audio file.
        """
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, selecting the language and SSML voice gender.
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)
        )

        # Select the type of audio file to return.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding.upper(), texttospeech.AudioEncoding.MP3)
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
    # Ensure the environment variable is set, e.g., from your .env file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-file.json"
    
    tts = GoogleTTSGenerator()
    sample_text = "Hello world! This is a sample text-to-speech conversion using Google Cloud TTS."
    output_path = tts.generate_voice(sample_text)
    print("Generated audio file:", output_path)
