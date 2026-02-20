"""
Prompt management endpoints for the Voice Cloning API.
"""

from fastapi import APIRouter, HTTPException

from voice_cloning.api.utils import get_timestamp

router = APIRouter()


@router.get("/prompts")
async def list_prompts():
    """
    List all cached voice prompts.
    
    Returns metadata for all created prompts in the current session.
    """
    from voice_cloning.api.main import app
    
    try:
        prompts = []
        for prompt_id, info in app.state.prompt_store.items():
            prompts.append({
                "prompt_id": prompt_id,
                "prompt_name": info["prompt_name"],
                "audio_duration": info["audio_duration"],
                "created_at": info["created_at"],
                "device": info["device"],
                "dtype": info["dtype"]
            })
        
        return {
            "success": True,
            "count": len(prompts),
            "prompts": prompts,
            "timestamp": get_timestamp()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: str):
    """
    Delete a cached voice prompt.
    
    **Parameters:**
    - `prompt_id`: ID of the prompt to delete
    """
    from voice_cloning.api.main import app
    
    engine = app.state.engine
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        if prompt_id not in app.state.prompt_store:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        # Remove from store
        del app.state.prompt_store[prompt_id]
        
        # Clear from engine cache if available
        if hasattr(engine, 'prompt_cache') and prompt_id in engine.prompt_cache:
            del engine.prompt_cache[prompt_id]
        
        return {
            "success": True,
            "message": f"Prompt deleted: {prompt_id}",
            "timestamp": get_timestamp()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
