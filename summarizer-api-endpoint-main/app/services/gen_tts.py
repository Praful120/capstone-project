# import tempfile
# from tempfile import NamedTemporaryFile

# from gtts import gTTS


# def text_to_speech(text: str, lang="en", slow=False) -> str:
#     """
#     Convert text to speech using gTTS

#     :param text: Text to convert to speech
#     :param lang: Language for TTS 
#     :param slow: Slow speech flag
#     :return: Path to the saved audio file
#     """
#     try:
#         # Find OS's temp directory
#         temp_dir = tempfile.gettempdir()

#         # Create a temp file to store the audio stream
#         temp_file = NamedTemporaryFile(
#             delete=False, suffix=".mp3", dir=temp_dir)

#         tts = gTTS(text=text, lang=lang, slow=slow)
#         tts.save(temp_file.name)

#         return temp_file.name
#     except Exception as e:
#         raise RuntimeError(f"TTS Conversion failed: {str(e)}")


# if __name__ == "__main__":
#     input_text = """
#     This is a test of the text-to-speech conversion.
#     The quick brown fox jumps over the lazy dog.
#     """
#     audio_file = text_to_speech(input_text)
#     print(f"Audio file saved at: {audio_file}")


# This file contains the logic to generate the Text-to-Speech audio.

from gtts import gTTS
import io
import base64

def generate_tts_audio(text: str) -> str:
    """
    Generates Text-to-Speech audio from the given text and returns it as a base64 encoded string.

    Args:
        text: The text to convert to speech.

    Returns:
        A base64 encoded string representing the MP3 audio data, or an empty string if an error occurs.
    """
    try:
        # Create a gTTS object with the provided text. 'lang' is set to English.
        tts = gTTS(text=text, lang='en', slow=False)

        # Use an in-memory binary stream to save the audio file.
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        # Reset the stream position to the beginning.
        audio_fp.seek(0)

        # Read the audio data from the stream.
        audio_bytes = audio_fp.read()
        
        # Encode the binary audio data into a base64 string.
        base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

        return base64_audio
    except Exception as e:
        # Print any errors that occur during the process.
        print(f"Error generating TTS audio: {e}")
        return ""


# test test