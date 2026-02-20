"""
Health check endpoints for the Voice Cloning API.
"""

from fastapi import APIRouter, HTTPException

from voice_cloning.api.models import EngineStatus
from voice_cloning.api.utils import get_timestamp

router = APIRouter()


@router.get("/health", response_model=EngineStatus)
async def health_check():
    """
    Check the health status of the API and engine.
    
    Returns engine status, device info, and available features.
    """
    from fastapi import Request
    from fastapi.requests import Request
    
    # Access app state through context
    try:
        # This is a workaround - in practice you'd pass app state through dependency
        from voice_cloning.api.main import app
        
        if app.state.engine is None:
            raise HTTPException(status_code=503, detail="Engine not initialized")
        
        engine = app.state.engine
        cached_prompts = list(app.state.prompt_store.keys())
        available_languages = engine.get_supported_languages()
        
        return EngineStatus(
            status="healthy",
            device=engine.device,
            dtype=str(engine.dtype),
            model_loaded=True,
            cached_prompts=cached_prompts,
            available_languages=available_languages,
            timestamp=get_timestamp()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
