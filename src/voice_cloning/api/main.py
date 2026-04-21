"""
FastAPI application for Voice Cloning Engine.

Main application file that sets up FastAPI, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import traceback
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# ============================================================================
# Application Factory
# ============================================================================

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Voice Cloning API",
        description="API for creating voice clones and synthesizing speech",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global state
    app.state.engine = None
    app.state.prompt_store = {}
    app.state.output_dir = Path("./api_output")
    app.state.temp_audio_dir = Path("./api_temp_audio")

    # Create necessary directories
    app.state.output_dir.mkdir(exist_ok=True)
    app.state.temp_audio_dir.mkdir(exist_ok=True)

    # Register event handlers
    @app.on_event("startup")
    async def startup_event():
        """Initialize the voice cloning engine on startup."""
        try:
            print("🚀 Initializing Voice Cloning Engine...")
            
            # Get recommended config and create engine
            config = get_recommended_config_for_hardware()
            print(f"📦 Using configuration: {config.preset}")
            print(f"   Device: {config.device}")
            print(f"   Data Type: {config.dtype}")
            
            # Determine model path
            model_path = None
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "../../models/voice-cloning-model"),
                os.path.join(os.path.dirname(__file__), "../../../models/voice-cloning-model"),
                "/content/models/voice-cloning-model",  # Colab path
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    print(f"✓ Found model at: {model_path}")
                    break
            
            if not model_path:
                raise FileNotFoundError(
                    f"Model not found in any of: {possible_paths}. "
                    "Please ensure the model is in the correct location."
                )
            
            app.state.engine = VoiceCloningEngine(
                model_path=model_path,
                device=config.device,
                dtype=config.dtype
            )
            print("✅ Engine initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize engine: {str(e)}")
            print(traceback.format_exc())
            raise

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown."""
        try:
            if app.state.engine:
                print("🔌 Shutting down Voice Cloning Engine...")
                if hasattr(app.state.engine, 'clear_prompt_cache'):
                    app.state.engine.clear_prompt_cache()
                del app.state.engine
                print("✅ Cleanup complete")
        except Exception as e:
            print(f"⚠️ Error during shutdown: {str(e)}")

    # Root endpoint
    @app.get("/")
    async def root():
        """API root endpoint with documentation links."""
        return {
            "name": "Voice Cloning API",
            "version": "1.0.0",
            "description": "API for creating voice clones and synthesizing speech",
            "documentation": {
                "swagger_ui": "/api/docs",
                "redoc": "/api/redoc",
                "openapi_schema": "/api/openapi.json"
            },
            "endpoints": {
                "health_check": "GET /api/v1/health",
                "create_prompt": "POST /api/v1/create-prompt",
                "synthesize": "POST /api/v1/synthesize",
                "download": "GET /api/v1/download/{filename}",
                "list_prompts": "GET /api/v1/prompts",
                "delete_prompt": "DELETE /api/v1/prompts/{prompt_id}"
            }
        }

    @app.get("/api/v1")
    async def api_root():
        """API v1 root endpoint."""
        return {
            "version": "1.0.0",
            "status": "active",
            "endpoints": {
                "health": "/api/v1/health",
                "create_prompt": "POST /api/v1/create-prompt",
                "synthesize": "POST /api/v1/synthesize",
                "download": "GET /api/v1/download/{filename}",
                "list_prompts": "GET /api/v1/prompts",
                "delete_prompt": "DELETE /api/v1/prompts/{prompt_id}"
            }
        }

    # Import and register routes
    from voice_cloning.api.routes import health, synthesis, management
    
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(synthesis.router, prefix="/api/v1", tags=["synthesis"])
    app.include_router(management.router, prefix="/api/v1", tags=["management"])

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
