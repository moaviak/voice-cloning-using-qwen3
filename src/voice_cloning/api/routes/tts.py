"""
Custom voice TTS endpoints for the Voice Cloning API.
"""

import io
import traceback

import soundfile as sf
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from voice_cloning.api.models import TTSRequest

router = APIRouter()


@router.post("/tts")
async def generate_tts(request: TTSRequest):
    """
    Generate speech from text using the custom-voice TTS model.

    Returns:
        Streamed WAV audio response.
    """
    from voice_cloning.api.main import app

    tts_model = getattr(app.state, "tts_model", None)
    if tts_model is None:
        raise HTTPException(status_code=503, detail="TTS model not initialized")

    try:
        if len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        wavs, sr = tts_model.generate_custom_voice(
            text=request.text,
            language=request.language,
            speaker=request.speaker,
        )

        if not wavs:
            raise HTTPException(status_code=500, detail="TTS generation returned no audio")

        buffer = io.BytesIO()
        sf.write(buffer, wavs[0], sr, format="WAV")
        buffer.seek(0)

        headers = {
            "X-TTS-Language": request.language,
            "X-TTS-Speaker": request.speaker,
            "Content-Disposition": 'attachment; filename="tts_output.wav"',
        }
        return StreamingResponse(
            buffer,
            media_type="audio/wav",
            headers=headers,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating TTS audio: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to generate TTS audio: {e}")
