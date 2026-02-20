"""
Full Workflow Example: End-to-End Voice Cloning

This example demonstrates a complete workflow:
1. Processing audio files
2. Creating voice clone prompts
3. Generating synthetic speech
4. Managing output files

This is a realistic example that you can adapt for your use case.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware
import numpy as np


def create_sample_workflow():
    """Create a sample workflow showing full voice cloning process."""
    
    print("=" * 70)
    print("Full Workflow: Voice Cloning End-to-End")
    print("=" * 70)
    
    # Step 1: Initialize engine
    print("\n[Step 1] Initialize Engine")
    print("-" * 70)
    
    config = get_recommended_config_for_hardware()
    print(f"Configuration:")
    print(f"  Device: {config.get_device_info()}")
    print(f"  Data type: {config.dtype}")
    print(f"  Sample rate: {config.sample_rate} Hz")
    print(f"  Output directory: {config.output_dir}")
    
    engine = VoiceCloningEngine(config)
    print("✓ Engine initialized")
    
    # Step 2: Create voice clone
    print("\n[Step 2] Create Voice Clone Prompt")
    print("-" * 70)
    print("""
To create a voice clone, you need:

1. Audio file (.wav format)
   - Recommended: 5-30 seconds of clear speech
   - Sample rate: 16kHz or 24kHz recommended
   - Mono or stereo (mono preferred)
   - Quality: Minimal background noise

2. Exact transcription/transcript
   - The exact text spoken in the audio
   - Proper punctuation and capitalization
   - Match the audio content precisely

Example code:
    prompt_id = engine.create_voice_clone_prompt(
        audio_path='voice_samples/john.wav',
        transcript='Hello, this is John speaking.',
        prompt_name='john_voice'
    )
    print(f'Voice clone created: {prompt_id}')
""")
    
    # Step 3: List cached prompts
    print("\n[Step 3] Manage Voice Prompts")
    print("-" * 70)
    print("""
Once prompts are created, manage them with:

    # List all cached prompts
    prompts = engine.list_cached_prompts()
    print(f'Cached prompts: {prompts}')
    
    # Synthesize with a specific prompt
    audio = engine.synthesize_voice(
        text='The new text to speak',
        language='English',
        prompt_name='john_voice'
    )
    
    # Save output
    import soundfile as sf
    output_path = 'output_john.wav'
    sf.write(output_path, audio, 24000)
    print(f'Audio saved to: {output_path}')
""")
    
    # Step 4: Batch processing
    print("\n[Step 4] Batch Processing")
    print("-" * 70)
    print("""
Process multiple texts with the same voice:

    texts = [
        'This is the first sentence.',
        'Here is the second sentence.',
        'And this is the third one.'
    ]
    
    for i, text in enumerate(texts):
        audio = engine.synthesize_voice(
            text=text,
            language='English',
            prompt_name='john_voice'
        )
        # Save each output
        output_path = f'output_{i:03d}.wav'
        sf.write(output_path, audio, 24000)
        print(f'Saved: {output_path}')
""")
    
    # Step 5: Memory management
    print("\n[Step 5] Memory Management")
    print("-" * 70)
    print("""
For production use, manage memory:

    # Check cached prompts
    cached = engine.list_cached_prompts()
    print(f'Memory usage - Cached prompts: {len(cached)}')
    
    # Clear cache if needed
    if len(cached) > 5:
        engine.clear_prompt_cache()
        print('Cache cleared')
""")
    
    # Step 6: Error handling
    print("\n[Step 6] Error Handling")
    print("-" * 70)
    print("""
Production-quality error handling:

    from pathlib import Path
    
    try:
        if not Path(audio_path).exists():
            raise FileNotFoundError(f'Audio file not found: {audio_path}')
        
        prompt_id = engine.create_voice_clone_prompt(
            audio_path=audio_path,
            transcript=transcript,
            prompt_name=prompt_name
        )
        print(f'✓ Voice clone created: {prompt_id}')
        
    except ValueError as e:
        print(f'✗ Invalid input: {e}')
    except RuntimeError as e:
        print(f'✗ Processing error: {e}')
    except Exception as e:
        print(f'✗ Unexpected error: {e}')
""")
    
    print("\n" + "=" * 70)
    print("Advanced Usage:"
    print("=" * 70)
    print("""
1. **Multiple Voices**: Create prompts for different speakers:
   - john_voice = engine.create_voice_clone_prompt(...)
   - jane_voice = engine.create_voice_clone_prompt(...)
   - Then use either when synthesizing

2. **Language Support**: 
   - Supported: Auto, English, Chinese, Japanese, Korean, 
               German, French, Russian, Portuguese, Spanish, Italian
   - Default: 'Auto' for automatic language detection

3. **Audio Processing**:
   - Use librosa for audio preprocessing
   - Normalize volume before cloning
   - Remove silence for better quality

4. **Integration with REST API**:
   - Use 02_api_client.py for REST API integration
   - Useful for web applications and services
   - Enables remote access to voice cloning
""")
    
    print("\n" + "=" * 70)
    print("Resources:")
    print("=" * 70)
    print("""
- Configuration: src/voice_cloning/config/__init__.py
- Engine: src/voice_cloning/core/__init__.py
- API: scripts/run_api.py
- Examples: examples/

Full documentation in: PROJECT_STRUCTURE.md, MIGRATION.md
""")


if __name__ == "__main__":
    create_sample_workflow()
