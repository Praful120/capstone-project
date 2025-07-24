import logging
import os
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.request_models import SummarizeRequest
from app.services.summarize import summarize
from app.services.gen_tts import text_to_speech

router = APIRouter()

@router.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        summary = summarize(request.text)

        if not summary:
            logging.error("Summary generation failed.")
            raise HTTPException(status_code=500, detail="Summary generation failed.")

        try:
            audio_path = text_to_speech(summary)
            audio_url = f"/audio/{os.path.basename(audio_path)}"
        except Exception as e:
            audio_url = None

        return {"summary": summary, "audio_url": audio_url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error occured during summarization: {str(e)}"
        )

@router.get('/audio')
async def get_audio_file(filename: str):
    raise NotImplementedError("TODO: Build a get endpoint for audio files.")

@router.get("/audio/{filename}")
async def get_audio(filename: str):
    try:
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, filename)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")

        if not filename.endswith('.mp3'):
            raise HTTPException(status_code=400, detail="Invalid file type")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving audio file: {str(e)}")

@router.get("/tts")
async def generate_and_serve_audio(text: str, lang: str = "en", slow: bool = False):
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text parameter cannot be empty")

        audio_path = text_to_speech(text, lang, slow)

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=os.path.basename(audio_path),
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(audio_path)}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating TTS audio: {str(e)}")
