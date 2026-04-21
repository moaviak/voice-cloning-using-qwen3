"""
Basic usage examples for Voice Cloning Engine.

These examples demonstrate how to use the VoiceCloningEngine directly.
For REST API examples, see api_examples.py.

Run examples:
    python examples/basic_examples.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware
import torch


def example_1_initialize_engine():
    """Example 1: Initialize the voice cloning engine."""
    print("\n" + "=" * 80)
    print("Example 1: Initialize the Voice Cloning Engine")
    print("=" * 80)
    
    # Get recommended configuration for your hardware
    config = get_recommended_config_for_hardware()
    print(f"Configuration: {config.preset}")
    print(f"Device: {config.device}")
    print(f"Data Type: {config.dtype}")
    
    try:
        # Initialize engine
        engine = VoiceCloningEngine(
            model_path="models/voice-cloning-model",  # Path to your model
            device=config.device,
            dtype=config.dtype
        )
        
        print(f"\n✅ Engine initialized successfully!")
        print(engine)
        
        return engine
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure the model is at 'models/voice-cloning-model/'")
        return None


def example_2_create_voice_prompt(engine):
    """Example 2: Create a voice clone prompt."""
    if engine is None:
        print("❌ Engine not initialized")
        return
    
    print("\n" + "=" * 80)
    print("Example 2: Create Voice Clone Prompt")
    print("=" * 80)
    print("""
To create a voice prompt, you need:
1. A WAV audio file with a sample of the speaker's voice (3-10 seconds)
2. The text transcription of what the speaker says in the audio

Example code:
    prompt_name = engine.create_voice_clone_prompt(
        audio_path="path/to/reference_audio.wav",
        transcript="This is the text spoken in the audio file.",
        prompt_name="my_voice_clone"
    )
    
    print(f"Created prompt: {prompt_name}")

The prompt is now cached and can be used for synthesis.
""")


def example_3_synthesize_voice(engine):
    """Example 3: Synthesize voice using a prompt."""
    if engine is None:
        print("❌ Engine not initialized")
        return
    
    print("\n" + "=" * 80)
    print("Example 3: Synthesize Voice")
    print("=" * 80)
    print("""
Once you have a prompt, you can synthesize speech:

Example code:
    audio, sr = engine.synthesize_voice(
        text="Hello, this is a synthesized voice using voice cloning!",
        language="English",
        prompt_name="my_voice_clone",
        output_path="output/cloned_voice.wav"
    )
    
    print(f"Generated audio: {len(audio)} samples at {sr} Hz")

The audio is automatically saved to the output path.
""")


def example_4_batch_synthesis(engine):
    """Example 4: Batch synthesis."""
    if engine is None:
        print("❌ Engine not initialized")
        return
    
    print("\n" + "=" * 80)
    print("Example 4: Batch Synthesis")
    print("=" * 80)
    print("""
You can synthesize multiple texts at once:

Example code:
    texts = [
        "Hello world",
        "This is a test",
        "Voice cloning is amazing!"
    ]
    
    wavs, sr = engine.synthesize_voice(
        text=texts,
        language="English",
        prompt_name="my_voice_clone"
    )
    
    print(f"Generated {len(wavs)} audio files")

This is faster than making individual requests.
""")


def example_5_manage_prompts(engine):
    """Example 5: Manage cached prompts."""
    if engine is None:
        print("❌ Engine not initialized")
        return
    
    print("\n" + "=" * 80)
    print("Example 5: Manage Cached Prompts")
    print("=" * 80)
    print(f"""
Prompts are cached in memory for fast reuse.

Example code:
    # List all cached prompts
    prompts = engine.list_cached_prompts()
    print(f"Cached prompts: {prompts}")
    
    # Get supported languages
    languages = engine.get_supported_languages()
    print(f"Supported languages: {languages}")
    
    # Clear a specific prompt
    engine.clear_prompt_cache("my_voice_clone")
    
    # Clear all prompts
    engine.clear_prompt_cache()

Current cached prompts: {engine.list_cached_prompts()}
Supported languages: {', '.join(engine.get_supported_languages())}
""")


def example_6_complete_workflow():
    """Example 6: Complete workflow."""
    print("\n" + "=" * 80)
    print("Example 6: Complete Workflow")
    print("=" * 80)
    print("""
Here's a complete workflow:

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# Step 1: Setup
config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(
    model_path="models/voice-cloning-model",
    device=config.device,
    dtype=config.dtype
)

# Step 2: Create voice prompt
prompt_name = engine.create_voice_clone_prompt(
    audio_path="reference_audio.wav",
    transcript="Reference text",
    prompt_name="my_voice"
)

# Step 3: Synthesize multiple texts
texts = [
    "Hello, welcome to the service",
    "How can I help you?",
    "Thank you, goodbye!"
]

for text in texts:
    audio, sr = engine.synthesize_voice(
        text=text,
        language="English",
        prompt_name=prompt_name,
        output_path=f"output/{text.replace(' ', '_')}.wav"
    )

# Step 4: Cleanup
engine.clear_prompt_cache()

print("✅ Workflow complete!")
""")


def main():
    """Run examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  Voice Cloning Engine - Basic Usage Examples".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Run examples
    engine = example_1_initialize_engine()
    example_2_create_voice_prompt(engine)
    example_3_synthesize_voice(engine)
    example_4_batch_synthesis(engine)
    example_5_manage_prompts(engine)
    example_6_complete_workflow()
    
    print("\n" + "=" * 80)
    print("📚 Documentation")
    print("=" * 80)
    print("""
For more information, see:
- docs/README.md - Main documentation
- docs/INSTALL.md - Installation guide
- docs/API.md - REST API documentation
- api/api_examples.py - REST API examples
- tests/ - Unit tests
""")


if __name__ == "__main__":
    main()
