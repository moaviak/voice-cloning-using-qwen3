"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any, Dict


class PromptResponse(BaseModel):
    """Response model for create-prompt endpoint."""
    success: bool
    prompt_id: str = Field(..., description="Server-side identifier for the prompt (for backward compatibility)")
    prompt_name: str = Field(..., description="Human-readable name for the prompt")
    message: str
    audio_duration: float = Field(..., description="Duration of input audio in seconds")
    sample_rate: int = Field(..., description="Sample rate of input audio")
    device: str = Field(..., description="Device used (cuda:0 or cpu)")
    dtype: str = Field(..., description="Data type used (float32 or bfloat16)")
    language: str = Field(..., description="Language associated with the reference audio")
    voice_clone_prompt: Dict[str, Any] = Field(
        ...,
        description="Raw prompt object as returned by the Qwen3-TTS model; "
        "this can be sent back to /synthesize for stateless usage."
    )
    timestamp: str = Field(..., description="ISO format timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "prompt_id": "cloned-voice-12345",
                "prompt_name": "my_voice_clone",
                "message": "Voice prompt created successfully",
                "audio_duration": 5.0,
                "sample_rate": 24000,
                "device": "cuda:0",
                "dtype": "bfloat16",
            "language": "English",
            "voice_clone_prompt": {
                "prompt_text": "internal prompt data from model",
                "spk_emb": [0.1, 0.2, 0.3],
            },
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class SynthesisRequest(BaseModel):
    """Request model for synthesis endpoint."""
    prompt_id: Optional[str] = Field(
        None,
        description=(
            "Legacy prompt identifier returned from create-prompt endpoint. "
            "Prefer sending `voice_clone_prompt` for stateless usage."
        ),
    )
    voice_clone_prompt: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Raw prompt object returned by the create-prompt endpoint. "
            "If provided, the server will synthesize directly from this "
            "object without relying on any server-side prompt storage."
        ),
    )
    text: str = Field(..., description="Text to synthesize")
    language: str = Field(
        "Auto",
        description=(
            "Target language for synthesis. Supported values: "
            "Auto, Chinese, English, Japanese, Korean, German, French, "
            "Russian, Portuguese, Spanish, Italian."
        ),
    )

    @model_validator(mode="after")
    def validate_prompt_source(self) -> "SynthesisRequest":
        """Ensure that at least one prompt source is provided."""
        if not self.prompt_id and self.voice_clone_prompt is None:
            raise ValueError("Either 'voice_clone_prompt' or 'prompt_id' must be provided")
        return self
    
    class Config:
        schema_extra = {
            "example": {
                "prompt_id": "cloned-voice-12345",
            "voice_clone_prompt": {
                "prompt_text": "internal prompt data from model",
            },
                "text": "Hello, this is a test of the voice cloning system.",
                "language": "English"
            }
        }


class SynthesisResponse(BaseModel):
    """Response model for synthesis endpoint."""
    success: bool
    message: str
    text: str
    language: str
    duration: float = Field(..., description="Duration of synthesized audio in seconds")
    device: str = Field(..., description="Device used (cuda:0 or cpu)")
    audio_file: str = Field(..., description="Path or filename of generated audio")
    timestamp: str = Field(..., description="ISO format timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Audio synthesized successfully",
                "text": "Hello, this is a test of the voice cloning system.",
                "language": "English",
                "duration": 3.5,
                "device": "cuda:0",
                "audio_file": "synthesized_audio_12345.wav",
                "timestamp": "2024-01-15T10:35:00"
            }
        }


class EngineStatus(BaseModel):
    """Response model for health check endpoint."""
    status: str
    device: str
    dtype: str
    model_loaded: bool
    cached_prompts: List[str]
    available_languages: List[str]
    timestamp: str


class ErrorResponse(BaseModel):
    """Response model for errors."""
    success: bool = False
    error: str
    details: Optional[str] = None
    timestamp: str
