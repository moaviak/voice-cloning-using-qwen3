"""
Custom voice TTS endpoints for the Voice Cloning API.
"""

import io
import traceback

import numpy as np
import soundfile as sf
import torch
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from voice_cloning.api.models import TTSRequest
from voice_cloning.api.utils import run_inference

router = APIRouter()

BATCH_SIZE = 50
SILENCE_DUR = 0.3


@router.post("/tts")
async def generate_tts(request: TTSRequest):
    """
    Generate speech from one or more texts using the custom-voice TTS model.

    Texts are processed in batches, concatenated with short silence gaps,
    and returned as a single WAV stream.

    Returns:
        Streamed WAV audio response.
    """
    from voice_cloning.api.main import app

    tts_model = getattr(app.state, "tts_model", None)
    if tts_model is None:
        raise HTTPException(status_code=503, detail="TTS model not initialized")

    try:
        texts = request.text
        all_wavs: list[np.ndarray] = []
        sr = None

        for i in range(0, len(texts), BATCH_SIZE):
            chunk = texts[i : i + BATCH_SIZE]

            wavs, batch_sr = await run_inference(
                tts_model.generate_custom_voice,
                text=chunk,
                language=request.language,
                speaker=request.speaker,
            )

            if not wavs:
                raise HTTPException(status_code=500, detail="TTS generation returned no audio")

            sr = batch_sr

            for j, wav in enumerate(wavs):
                all_wavs.append(wav)
                if j < len(wavs) - 1:
                    all_wavs.append(np.zeros(int(sr * SILENCE_DUR), dtype=wav.dtype))
            all_wavs.append(np.zeros(int(sr * SILENCE_DUR), dtype=wavs[-1].dtype))

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        combined = np.concatenate(all_wavs, axis=0)

        buffer = io.BytesIO()
        sf.write(buffer, combined, sr, format="WAV")
        buffer.seek(0)

        headers = {
            "X-TTS-Language": request.language,
            "X-TTS-Speaker": request.speaker,
            "X-TTS-Text-Count": str(len(texts)),
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
