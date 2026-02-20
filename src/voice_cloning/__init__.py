"""
Voice Cloning Package

A comprehensive voice cloning system built with Qwen3-TTS.

Modules:
    - core: Voice cloning engine and core functionality
    - config: Configuration management and presets
    - api: FastAPI application and endpoints
    - utils: Shared utilities for audio processing and helpers

Example:
    >>> from voice_cloning.core import VoiceCloningEngine
    >>> from voice_cloning.config import get_recommended_config_for_hardware
    >>>
    >>> config = get_recommended_config_for_hardware()
    >>> engine = VoiceCloningEngine(
    ...     model_path="path/to/model",
    ...     device=config.device,
    ...     dtype=config.dtype
    ... )
    >>>
    >>> # Create voice prompt
    >>> engine.create_voice_clone_prompt(
    ...     audio_path="reference.wav",
    ...     transcript="Your voice sample",
    ...     prompt_name="my_voice"
    ... )
    >>>
    >>> # Synthesize speech
    >>> audio, sr = engine.synthesize_voice(
    ...     text="Hello world",
    ...     language="English",
    ...     prompt_name="my_voice"
    ... )
"""

__version__ = "1.0.0"
__author__ = "Voice Cloning Team"
__all__ = [
    "VoiceCloningEngine",
    "get_recommended_config_for_hardware",
    "EngineConfig",
]

try:
    from voice_cloning.core import VoiceCloningEngine
    from voice_cloning.config import (
        EngineConfig,
        get_recommended_config_for_hardware,
    )
except ImportError:
    # Allow imports to fail gracefully if dependencies aren't installed
    pass
