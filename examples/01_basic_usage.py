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
    
    # Step 3: Create a voice clone prompt using sample audio
    print("\n[3/4] Creating voice clone prompt...")
    audio_path = Path(__file__).parent / "sample_audios" / "1.wav"
    transcript = (
        "Please call Stella. Ask her to bring these things with her from the store: "
        "Six spoons of fresh snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob. "
        "We also need a small plastic snake and a big toy frog for the kids. "
        "She can scoop these things into three red bags, and we will go meet her Wednesday at the train station."
    )
    
    if audio_path.exists():
        print(f"  Using sample audio: {audio_path}")
        print(f"  Transcript: {transcript[:80]}...")
        try:
            # Create a language-aware voice clone prompt and capture the raw
            # prompt object so it can be reused or sent over the network.
            language = "English"
            voice_clone_prompt = engine.create_voice_clone_prompt(
                audio_path=str(audio_path),
                transcript=transcript,
                prompt_name="sample_voice",
            )
            print(f"✓ Voice clone created for language='{language}'")
        except Exception as e:
            print(f"✗ Error creating voice clone: {e}")
            return
    else:
        print(f"✗ Sample audio not found at: {audio_path}")
        print("  Please ensure the sample_audios/1.wav file exists.")
        return
    
    # Step 4: Synthesize audio using the clone
    print("\n[4/4] Synthesizing audio with cloned voice...")
    try:
        synthesis_text = "Hello everyone, this is a test of voice cloning technology."
        print(f"  Synthesis text: {synthesis_text}")
        # Here we pass the raw prompt object returned above. This is the same
        # object that the API now returns from /create-prompt and expects in
        # the /synthesize request body.
        result = engine.synthesize_voice(
            text=synthesis_text,
            language="English",
            voice_clone_prompt=voice_clone_prompt,
            prompt_name="sample_voice",
        )
        
        # Handle both tuple and array returns
        if isinstance(result, tuple):
            audio_output, sample_rate = result
        else:
            audio_output = result
            sample_rate = 24000
        
        print(f"✓ Audio synthesized successfully")
        print(f"  Output shape: {audio_output.shape}")
        print(f"  Sample rate: {sample_rate} Hz")
    except Exception as e:
        print(f"✗ Error synthesizing audio: {e}")
    
    # List available methods
    print("\n" + "=" * 70)
    print("Available Engine Methods:")
    print("=" * 70)
    
    methods = [
        ("create_voice_clone_prompt(audio_path, transcript, prompt_name)", 
         "Create a reusable voice clone from audio + transcript and return the raw prompt object"),
        ("synthesize_voice(text, language, prompt_name=None, voice_clone_prompt=None)", 
         "Synthesize audio using either a stored prompt by name or a raw voice_clone_prompt object"),
        ("list_cached_prompts()", 
         "List all currently cached voice prompts"),
        ("clear_prompt_cache()", 
         "Clear all cached prompts and free memory"),
    ]
    
    for i, (method, desc) in enumerate(methods, 1):
        print(f"\n{i}. {method}")
        print(f"   {desc}")
    
    # Show cached prompts
    print("\n" + "=" * 70)
    print("Cached Prompts:")
    print("=" * 70)
    cached = engine.list_cached_prompts()
    if cached:
        for prompt in cached:
            print(f"  - {prompt}")
    else:
        print("  No cached prompts")
    
    print("\n" + "=" * 70)
    print("\nFor more examples, see:")
    print("  - 02_api_client.py: Using REST API endpoints")
    print("  - 03_full_workflow.py: End-to-end example with files")
    print("  - 04_batch_processing.py: Batch synthesis examples")
    print("=" * 70)


if __name__ == "__main__":
    main()
