"""
Basic Usage Example: Direct Engine Usage

This example shows how to use the VoiceCloningEngine directly without the REST API.
Demonstrates:
1. Initializing the engine with auto hardware detection
2. Creating a voice clone prompt from audio + transcript
3. Synthesizing audio using the stored clone prompt

Requirements:
- Audio file (.wav format) for voice cloning
- Reference transcript for the audio
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware


def main():
    """Main example function."""
    
    print("=" * 70)
    print("Voice Cloning Engine - Basic Usage Example")
    print("=" * 70)
    
    # Step 1: Get recommended config for your hardware
    print("\n[1/4] Getting recommended configuration for your hardware...")
    config = get_recommended_config_for_hardware()
    print(f"✓ Using device: {config.get_device_info()}")
    print(f"✓ Data type: {config.dtype}")
    
    # Step 2: Initialize the engine
    print("\n[2/4] Initializing Voice Cloning Engine...")
    engine = VoiceCloningEngine(config)
    print("✓ Engine initialized successfully")
    
    # Step 3: Create a voice clone prompt
    # NOTE: You'll need to provide actual audio and transcript files
    print("\n[3/4] Creating voice clone prompt...")
    print("  To use this example, you need:")
    print("  - A .wav audio file with someone speaking")
    print("  - The exact transcript/text that was spoken")
    print("\n  Example code:")
    print("  ```python")
    print("  prompt_name = engine.create_voice_clone_prompt(")
    print("      audio_path='path/to/audio.wav',")
    print("      transcript='Hello, this is my voice for cloning.',")
    print("      prompt_name='my_voice'")
    print("  )")
    print("  ```")
    
    # Step 4: Synthesize audio using the clone
    print("\n[4/4] Synthesizing audio with cloned voice...")
    print("  Once you have a prompt cached, generate speech with:")
    print("  ```python")
    print("  audio_output = engine.synthesize_voice(")
    print("      text='The text you want to synthesize',")
    print("      language='Auto',  # 'English', 'Chinese', etc.")
    print("      prompt_name='my_voice'")
    print("  )")
    print("  ```")
    
    # List available methods
    print("\n" + "=" * 70)
    print("Available Engine Methods:")
    print("=" * 70)
    
    methods = [
        ("create_voice_clone_prompt(audio_path, transcript, prompt_name)", 
         "Create a reusable voice clone from audio + transcript"),
        ("synthesize_voice(text, language, prompt_name)", 
         "Synthesize audio using a stored voice clone"),
        ("list_cached_prompts()", 
         "List all currently cached voice prompts"),
        ("clear_prompt_cache()", 
         "Clear all cached prompts and free memory"),
    ]
    
    for i, (method, desc) in enumerate(methods, 1):
        print(f"\n{i}. {method}")
        print(f"   {desc}")
    
    print("\n" + "=" * 70)
    print("\nFor more examples, see:")
    print("  - 02_api_client.py: Using REST API endpoints")
    print("  - 03_full_workflow.py: End-to-end example with files")
    print("  - 04_batch_processing.py: Batch synthesis examples")
    print("=" * 70)


if __name__ == "__main__":
    main()
