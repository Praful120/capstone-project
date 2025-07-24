from gtts import gTTS
import tempfile
import os

def text_to_speech(text, lang="en", slow=False):
    """
    Convert given text to speech using gTTS and return path to saved .mp3 file.
    """
    tts = gTTS(text=text, lang=lang, slow=slow)
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "speech.mp3")
    tts.save(audio_path)
    return audio_path
