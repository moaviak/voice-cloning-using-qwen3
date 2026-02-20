"""
Voice Cloning Examples

This package contains comprehensive examples demonstrating how to use
the Voice Cloning Engine and REST API.

Examples:
---------

1. **01_basic_usage.py**: Direct engine usage
   - Initialize the engine
   - Create voice clones
   - Synthesize audio
   
2. **02_api_client.py**: REST API client usage
   - Start the API server
   - Create voice clones via HTTP
   - Synthesize audio via HTTP
   - Manage prompts via REST API
   
3. **03_full_workflow.py**: End-to-end workflow
   - Complete voice cloning pipeline
   - Best practices and patterns
   - Error handling
   - Memory management
   
4. **04_batch_processing.py**: Batch operations
   - Process multiple audio files
   - Synthesize multiple texts
   - Production pipeline patterns
   - Logging and progress tracking

Quick Start:
-----------

**Option 1: Direct Engine Usage**

    from voice_cloning import VoiceCloningEngine
    from voice_cloning.config import get_recommended_config_for_hardware
    
    config = get_recommended_config_for_hardware()
    engine = VoiceCloningEngine(config)
    
    # Create voice clone
    prompt_id = engine.create_voice_clone_prompt(
        audio_path='voice.wav',
        transcript='Hello, this is my voice.',
        prompt_name='my_voice'
    )
    
    # Synthesize audio
    audio = engine.synthesize_voice(
        text='Some new text',
        language='English',
        prompt_name='my_voice'
    )

**Option 2: REST API**

    # Start server
    python scripts/run_api.py --port 8000
    
    # Use API client
    from examples.api_client import VoiceCloningAPIClient
    
    client = VoiceCloningAPIClient()
    
    # Create voice clone
    response = client.create_voice_clone(
        audio_file='voice.wav',
        transcript='Hello, this is my voice.',
        prompt_name='my_voice'
    )
    
    # Synthesize audio
    audio_data = client.synthesize_audio(
        text='Some new text',
        prompt_name='my_voice'
    )

Requirements:
-------------

    pip install torch
    pip install qwen-tts
    pip install numpy
    pip install soundfile
    pip install fastapi
    pip install uvicorn
    pip install requests

Running Examples:
-----------------

    # Basic usage
    python examples/01_basic_usage.py
    
    # API client (requires server running)
    python scripts/run_api.py &
    python examples/02_api_client.py
    
    # Full workflow
    python examples/03_full_workflow.py
    
    # Batch processing
    python examples/04_batch_processing.py

For more information, see PROJECT_STRUCTURE.md and MIGRATION.md
"""

__all__ = [
    "VoiceCloningAPIClient",
    "BatchVoiceCloningProcessor",
]

# Import key classes if needed
try:
    from .api_client import VoiceCloningAPIClient
    from .batch_processing import BatchVoiceCloningProcessor
except ImportError:
    pass
