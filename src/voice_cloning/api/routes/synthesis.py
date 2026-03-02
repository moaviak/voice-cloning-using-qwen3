"""
Voice synthesis endpoints for the Voice Cloning API.
"""

import io
import os
import uuid
import traceback
import base64
import pickle
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse

import soundfile as sf

from voice_cloning.api.models import PromptResponse, SynthesisRequest, SynthesisResponse
from voice_cloning.api.utils import get_timestamp, cleanup_file

router = APIRouter()


@router.post("/create-prompt", response_model=PromptResponse)
async def create_prompt(
    audio: UploadFile = File(..., description="Reference audio file (.wav format)"),
    transcript: str = Form(..., description="Transcription of the audio"),
    prompt_name: str = Form(None, description="Custom name for the prompt"),
    language: str = Form(
        "Auto",
        description=(
            "Language of the reference audio. Supported values: "
            "Auto, Chinese, English, Japanese, Korean, German, French, "
            "Russian, Portuguese, Spanish, Italian."
        ),
    ),
):
    """
    Create a voice clone prompt from reference audio and transcript.
    
    This endpoint generates a voice prompt that captures the speaker's voice
    characteristics. The prompt can then be used to synthesize speech in that voice.
    
    **Parameters:**
    - `audio`: WAV audio file containing the reference voice sample (required)
    - `transcript`: Text transcription of what is spoken in the audio (required)
    - `prompt_name`: Optional custom name for the prompt (auto-generated if not provided)
    - `language`: Language of the reference audio (for metadata and downstream usage)
    
    **Returns:**
    - `prompt_id`: Unique identifier for this prompt
    - `prompt_name`: Name of the created prompt
    - `audio_duration`: Duration of input audio in seconds
    - `device`: Device used for processing (cuda:0 or cpu)
    - `dtype`: Data type used (float32 or bfloat16)
    """
    from voice_cloning.api.main import app
    
    engine = app.state.engine
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        # Validate file
        if audio.content_type not in ["audio/wav", "audio/x-wav", "application/octet-stream"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Please upload a WAV file."
            )
        
        if len(transcript.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty"
            )
        
        # Read audio file
        contents = await audio.read()
        audio_bytes = io.BytesIO(contents)
        
        # Load audio
        audio_data, sr = sf.read(audio_bytes)
        
        # Validate audio
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty")
        
        if sr != 24000:
            print(f"⚠️ Audio sample rate is {sr}, expected 24000 Hz")
        
        # Generate prompt ID and name
        prompt_id = str(uuid.uuid4())[:8] + "-" + "__import__('datetime').datetime.now().strftime('%Y%m%d%H%M%S')"
        if prompt_name is None:
            prompt_name = f"voice_clone_{prompt_id}"
        
        # Save audio temporarily
        temp_audio_path = app.state.temp_audio_dir / f"ref_audio_{prompt_id}.wav"
        sf.write(str(temp_audio_path), audio_data, sr)
        
        # Create voice clone prompt
        print(f"🎤 Creating voice prompt: {prompt_id}")
        voice_clone_prompt = engine.create_voice_clone_prompt(
            audio_path=str(temp_audio_path),
            transcript=transcript,
            prompt_name=prompt_name
        )
        # Serialize prompt object to a base64-encoded string so it can be
        # safely transported over JSON without tensor serialization issues.
        try:
            encoded_prompt = base64.b64encode(pickle.dumps(voice_clone_prompt)).decode("utf-8")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to serialize voice clone prompt: {e}",
            )
        
        # Store prompt metadata
        audio_duration = len(audio_data) / sr
        app.state.prompt_store[prompt_id] = {
            "prompt_name": prompt_name,
            "transcript": transcript,
            "audio_duration": audio_duration,
            "sample_rate": sr,
            "created_at": get_timestamp(),
            "device": engine.device,
            "dtype": str(engine.dtype),
            "language": language,
            "voice_clone_prompt": encoded_prompt,
        }
        
        print(f"✅ Prompt created: {prompt_id}")
        
        return PromptResponse(
            success=True,
            prompt_id=prompt_id,
            prompt_name=prompt_name,
            message="Voice prompt created successfully",
            audio_duration=audio_duration,
            sample_rate=sr,
            device=engine.device,
            dtype=str(engine.dtype),
            language=language,
            voice_clone_prompt=encoded_prompt,
            timestamp=get_timestamp()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error creating prompt: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create prompt: {str(e)}"
        )
    finally:
        await audio.close()


@router.post("/synthesize")
async def synthesize_voice(
    request: SynthesisRequest,
):
    """
    Synthesize speech using a voice clone prompt.
    
    This endpoint generates audio by synthesizing the provided text using
    the voice characteristics from a previously created clone prompt.
    
    **Parameters:**
    - `voice_clone_prompt`: Raw prompt object returned from /create-prompt
    - `prompt_id`: (Legacy) ID of a server-side stored prompt
    - `text`: Text to synthesize
    - `language`: Language code (default: English)
    
    **Returns:**
    - Streamed WAV audio as the HTTP response body
    """
    from voice_cloning.api.main import app
    
    engine = app.state.engine
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        # Validate text
        if len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Decide how to obtain the prompt
        voice_clone_prompt = None
        prompt_name = None

        # Preferred: stateless usage via voice_clone_prompt
        if request.voice_clone_prompt is not None:
            print("🎵 Synthesizing with provided voice_clone_prompt (stateless mode)")
            try:
                voice_clone_prompt = pickle.loads(
                    base64.b64decode(request.voice_clone_prompt.encode("utf-8"))
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to decode voice_clone_prompt: {e}",
                )
        else:
            # Backward-compatible path using stored prompt_id
            if not request.prompt_id or request.prompt_id not in app.state.prompt_store:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Prompt not found: {request.prompt_id}. "
                        "Either provide 'voice_clone_prompt' from /create-prompt "
                        "or create a prompt first using /api/v1/create-prompt"
                    ),
                )

            prompt_info = app.state.prompt_store[request.prompt_id]
            prompt_name = prompt_info["prompt_name"]
            encoded_prompt = prompt_info.get("voice_clone_prompt")

            if encoded_prompt is None:
                raise HTTPException(
                    status_code=500,
                    detail="Stored prompt missing 'voice_clone_prompt' data.",
                )

            try:
                voice_clone_prompt = pickle.loads(
                    base64.b64decode(encoded_prompt.encode("utf-8"))
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to decode stored voice_clone_prompt: {e}",
                )

            print(f"🎵 Synthesizing using stored prompt_id={request.prompt_id}, name={prompt_name}")

        # Generate audio in-memory
        print(f"🗣  Text: '{request.text[:50]}...' | Language: {request.language}")

        audio_data, sr = engine.synthesize_voice(
            text=request.text,
            language=request.language,
            voice_clone_prompt=voice_clone_prompt,
            prompt_name=prompt_name,
        )

        # Calculate duration
        duration = len(audio_data) / sr if audio_data is not None else 0

        # Serialize to WAV in-memory and stream back
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sr, format="WAV")
        buffer.seek(0)

        print(f"✅ Audio synthesized in-memory ({duration:.2f}s, {sr} Hz)")

        headers = {
            "X-Synthesis-Text": request.text[:200],
            "X-Synthesis-Language": request.language,
            "X-Synthesis-Duration": f"{duration:.4f}",
            "X-Synthesis-Device": str(engine.device),
            "Content-Disposition": 'attachment; filename="synthesized_audio.wav"',
        }

        return StreamingResponse(
            buffer,
            media_type="audio/wav",
            headers=headers,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error synthesizing voice: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to synthesize voice: {str(e)}"
        )


@router.get("/download/{filename}")
async def download_audio(filename: str, background_tasks: BackgroundTasks):
    """
    Download synthesized audio file.
    
    **Parameters:**
    - `filename`: Name of the file returned from /api/v1/synthesize
    
    **Returns:**
    - Audio file (WAV format)
    """
    from voice_cloning.api.main import app
    
    try:
        filepath = app.state.output_dir / filename
        
        if not filepath.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Validate path to prevent directory traversal
        if not str(filepath.resolve()).startswith(str(app.state.output_dir.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Schedule cleanup after 1 hour
        background_tasks.add_task(cleanup_file, str(filepath), 3600)
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="audio/wav"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
