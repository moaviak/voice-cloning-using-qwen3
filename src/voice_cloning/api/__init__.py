"""
FastAPI application package for Voice Cloning Engine.

Provides REST API endpoints for voice cloning and synthesis operations.

Main modules:
    - main: FastAPI application factory and configuration
    - routes: API endpoint definitions
      - health: Health check endpoint
      - synthesis: Create prompt and synthesize endpoints
      - management: Prompt management endpoints
    - models: Pydantic request/response models
    - utils: Utility functions
"""

from voice_cloning.api.main import app, create_app

__all__ = ["app", "create_app"]
