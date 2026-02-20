"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class PromptResponse(BaseModel):
    """Response model for create-prompt endpoint."""
    success: bool
    prompt_id: str
    prompt_name: str
    message: str
    audio_duration: float = Field(..., description="Duration of input audio in seconds")
    sample_rate: int = Field(..., description="Sample rate of input audio")
    device: str = Field(..., description="Device used (cuda:0 or cpu)")
    dtype: str = Field(..., description="Data type used (float32 or bfloat16)")
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
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class SynthesisRequest(BaseModel):
    """Request model for synthesis endpoint."""
    prompt_id: str = Field(..., description="The prompt ID returned from create-prompt endpoint")
    text: str = Field(..., description="Text to synthesize")
    language: str = Field("English", description="Language code (English, Chinese, Spanish, etc.)")
    
    class Config:
        schema_extra = {
            "example": {
                "prompt_id": "cloned-voice-12345",
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
