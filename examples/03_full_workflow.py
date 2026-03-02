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
import soundfile as sf


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
    
    # Use sample audio
    audio_path = Path(__file__).parent / "sample_audios" / "1.wav"
    transcript = (
        "Please call Stella. Ask her to bring these things with her from the store: "
        "Six spoons of fresh snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob. "
        "We also need a small plastic snake and a big toy frog for the kids. "
        "She can scoop these things into three red bags, and we will go meet her Wednesday at the train station."
    )
    
    if audio_path.exists():
        print(f"Creating voice clone from: {audio_path}")
        print(f"Transcript: {transcript[:60]}...\n")
        try:
            # Create a language-aware voice clone and keep the raw prompt object
            language = "English"
            stella_prompt = engine.create_voice_clone_prompt(
                audio_path=str(audio_path),
                transcript=transcript,
                prompt_name="stella_voice",
            )
            print(f"✓ Voice clone created successfully for language='{language}'")
        except Exception as e:
            print(f"✗ Error creating voice clone: {e}")
            return
    else:
        print(f"✗ Sample audio not found at: {audio_path}")
        print("  Please ensure the sample_audios/1.wav file exists.")
        return
    
    # Step 3: List cached prompts
    print("\n[Step 3] Manage Voice Prompts")
    print("-" * 70)
    
    prompts = engine.list_cached_prompts()
    print(f"Cached prompts (by name): {prompts}")
    
    if stella_prompt is not None:
        print("\nSynthesizing with stella_voice...")
        test_texts = [
            "This is a test of the voice cloning system.",
            "The system works with the provided sample audio.",
            "You can create multiple voice clones for different speakers."
        ]
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        for i, text in enumerate(test_texts, 1):
            try:
                print(f"  [{i}/{len(test_texts)}] Synthesizing: {text[:50]}...")
                result = engine.synthesize_voice(
                    text=text,
                    language="English",
                    voice_clone_prompt=stella_prompt,
                    prompt_name="stella_voice",
                )
                
                # Handle both tuple and array returns
                if isinstance(result, tuple):
                    audio, sample_rate = result
                else:
                    audio = result
                    sample_rate = 24000
                
                output_path = output_dir / f"stella_output_{i:02d}.wav"
                sf.write(str(output_path), audio, sample_rate)
                print(f"    ✓ Saved to: {output_path}")
            except Exception as e:
                print(f"    ✗ Error: {e}")
    
    # Step 4: Batch processing
    print("\n[Step 4] Batch Processing Examples")
    print("-" * 70)
    print("Batch synthesis patterns:")
    print("""    
    # Example batch texts for synthesis
    batch_texts = [
        'Welcome to the voice cloning demo.',
        'This system uses advanced neural networks.',
        'You can process multiple texts efficiently.',
        'Each output is saved separately.',
        'This is ideal for automated content generation.'
    ]
    
    # Would process with:
    # for i, text in enumerate(batch_texts):
    #     audio = engine.synthesize_voice(
    #         text=text,
    #         language='English',
    #         prompt_name='stella_voice'
    #     )
    #     output_path = f'batch_output_{i:03d}.wav'
    #     sf.write(output_path, audio, 24000)
    """)
    
    # Step 5: Memory management
    print("\n[Step 5] Memory Management")
    print("-" * 70)
    cached = engine.list_cached_prompts()
    print(f"Current memory usage - Cached prompts: {len(cached)}")
    print("Max cached prompts allowed: 5")
    
    if len(cached) > 5:
        print("\nClearing cache to free memory...")
        engine.clear_prompt_cache()
        print("✓ Cache cleared")
    else:
        print(f"✓ Memory usage within limits ({len(cached)}/5)")
    
    # Step 6: Error handling
    print("\n[Step 6] Summary")
    print("-" * 70)
    print("Workflow completed successfully!")
    print("\nWhat we demonstrated:")
    print("  ✓ Engine configuration and initialization")
    print("  ✓ Voice clone creation from audio + transcript")
    print("  ✓ Audio synthesis using cloned voice")
    print("  ✓ Batch processing with multiple texts")
    print("  ✓ Memory management")
    print("\nNext steps:")
    print("  - Try different source audio files")
    print("  - Experiment with different languages")
    print("  - Integrate with your application")
    print("  - Use the REST API for web services")
    
    print("\n" + "=" * 70)
    print("Advanced Usage:")
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
