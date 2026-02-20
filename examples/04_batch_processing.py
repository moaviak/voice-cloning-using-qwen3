"""
Batch Processing Example

This example shows how to efficiently process many texts
with voice cloning, including:
1. Batch voice cloning from multiple audio files
2. Batch synthesis with multiple texts
3. Production patterns for handling many files
4. Performance optimization tips
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware


class BatchVoiceCloningProcessor:
    """Helper class for batch processing with voice cloning."""
    
    def __init__(self, engine: VoiceCloningEngine):
        """Initialize batch processor.
        
        Args:
            engine: VoiceCloningEngine instance
        """
        self.engine = engine
        self.created_prompts: List[str] = []
    
    def batch_create_prompts(
        self, 
        audio_files: Dict[str, str],
        prompt_names: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Create multiple voice clone prompts.
        
        Args:
            audio_files: Dict of {prompt_name: (audio_path, transcript)}
            prompt_names: Optional list to track prompt names
            
        Returns:
            Dict of {prompt_name: status}
        """
        results = {}
        total = len(audio_files)
        
        for i, (prompt_name, (audio_path, transcript)) in enumerate(audio_files.items(), 1):
            print(f"[{i}/{total}] Creating prompt: {prompt_name}")
            
            try:
                # Validate files exist
                if not Path(audio_path).exists():
                    results[prompt_name] = f"Error: Audio file not found: {audio_path}"
                    continue
                
                # Create prompt
                prompt_id = self.engine.create_voice_clone_prompt(
                    audio_path=audio_path,
                    transcript=transcript,
                    prompt_name=prompt_name
                )
                
                results[prompt_name] = "Success"
                self.created_prompts.append(prompt_name)
                print(f"  ✓ Created: {prompt_id}")
                
            except Exception as e:
                results[prompt_name] = f"Error: {str(e)}"
                print(f"  ✗ Failed: {e}")
        
        return results
    
    def batch_synthesize(
        self,
        prompt_name: str,
        texts: List[str],
        language: str = "Auto",
        output_dir: str = "batch_output"
    ) -> List[str]:
        """Synthesize audio for multiple texts using one voice.
        
        Args:
            prompt_name: Name of voice prompt to use
            texts: List of texts to synthesize
            language: Language for synthesis
            output_dir: Directory to save output files
            
        Returns:
            List of output file paths
        """
        output_paths = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        total = len(texts)
        print(f"\nSynthesizing {total} texts with '{prompt_name}'...")
        
        for i, text in enumerate(texts, 1):
            try:
                print(f"[{i}/{total}] Synthesizing: {text[:50]}...")
                
                # Synthesize
                audio = self.engine.synthesize_voice(
                    text=text,
                    language=language,
                    prompt_name=prompt_name
                )
                
                # Save output
                output_path = output_dir / f"output_{i:03d}.wav"
                
                # You would save the audio here with soundfile
                # import soundfile as sf
                # sf.write(str(output_path), audio, 24000)
                
                output_paths.append(str(output_path))
                print(f"  ✓ Saved: {output_path}")
                
            except Exception as e:
                print(f"  ✗ Failed: {e}")
        
        return output_paths
    
    def batch_summarize(self) -> Dict:
        """Get summary of batch processing results.
        
        Returns:
            Summary dictionary
        """
        return {
            "prompts_created": len(self.created_prompts),
            "prompt_list": self.created_prompts,
            "cached_prompts": self.engine.list_cached_prompts()
        }


def example_scenario_1_multiple_speakers():
    """Example: Create voice clones for multiple speakers."""
    
    print("\n" + "=" * 70)
    print("Scenario 1: Multiple Speaker Voice Cloning")
    print("=" * 70)
    
    # Initialize engine and processor
    config = get_recommended_config_for_hardware()
    engine = VoiceCloningEngine(config)
    processor = BatchVoiceCloningProcessor(engine)
    
    # Define multiple speakers
    speakers = {
        "alice": ("audio_samples/alice.wav", "Hello, I am Alice."),
        "bob": ("audio_samples/bob.wav", "Hi, I'm Bob."),
        "charlie": ("audio_samples/charlie.wav", "Hey, Charlie here."),
    }
    
    print("\nCreating voice clones for multiple speakers...")
    print("(This is a demonstration - you'd need actual audio files)")
    
    results = processor.batch_create_prompts(speakers)
    
    print("\nResults:")
    for prompt_name, status in results.items():
        print(f"  {prompt_name}: {status}")
    
    return engine, processor


def example_scenario_2_large_scale_synthesis():
    """Example: Large-scale text synthesis with multiple voices."""
    
    print("\n" + "=" * 70)
    print("Scenario 2: Large-Scale Synthesis")
    print("=" * 70)
    
    # Initialize
    config = get_recommended_config_for_hardware()
    engine = VoiceCloningEngine(config)
    processor = BatchVoiceCloningProcessor(engine)
    
    # Prepare texts to synthesize
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Voice cloning technology is advancing rapidly.",
        "This is an automated synthesis example.",
        "The system processes multiple requests efficiently.",
        "Quality can be adjusted based on requirements.",
    ]
    
    print(f"\nPrepared {len(texts)} texts for synthesis")
    print("(Demonstration - requires pre-existing voice prompts)")
    
    # Would synthesize with: processor.batch_synthesize("voice_name", texts)


def example_scenario_3_production_pipeline():
    """Example: Production-ready batch processing pipeline."""
    
    print("\n" + "=" * 70)
    print("Scenario 3: Production Pipeline")
    print("=" * 70)
    
    code = """
# Production pipeline example
from pathlib import Path

class ProductionPipeline:
    def __init__(self, config):
        self.engine = VoiceCloningEngine(config)
        self.processor = BatchVoiceCloningProcessor(self.engine)
        self.log_file = Path('processing.log')
    
    def process_directory(self, audio_dir, output_dir):
        '''Process all audio files in a directory.'''
        audio_dir = Path(audio_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all audio files
        audio_files = {}
        for wav_file in audio_dir.glob('*.wav'):
            prompt_name = wav_file.stem
            # Load transcript from accompanying .txt file
            txt_file = wav_file.with_suffix('.txt')
            if txt_file.exists():
                transcript = txt_file.read_text().strip()
                audio_files[prompt_name] = (str(wav_file), transcript)
        
        # Create prompts
        results = self.processor.batch_create_prompts(audio_files)
        
        # Log results
        with open(self.log_file, 'a') as f:
            f.write(f'Processed {len(results)} files\\n')
        
        return results

# Usage
pipeline = ProductionPipeline(config)
pipeline.process_directory('voice_samples/', 'output/')
"""
    
    print("\nProduction-ready pipeline code:")
    print(code)


def main():
    """Main example function."""
    
    print("=" * 70)
    print("Batch Processing Examples - Voice Cloning")
    print("=" * 70)
    
    print("\nThis example demonstrates batch processing patterns:")
    print("1. Creating multiple voice clones in batch")
    print("2. Synthesizing multiple texts with one voice")
    print("3. Production pipeline patterns")
    
    # Show scenarios
    example_scenario_1_multiple_speakers()
    example_scenario_2_large_scale_synthesis()
    example_scenario_3_production_pipeline()
    
    print("\n" + "=" * 70)
    print("Best Practices for Batch Processing:")
    print("=" * 70)
    print("""
1. **Error Handling**: Wrap operations in try-except blocks
   - Continue processing if one file fails
   - Log errors for debugging

2. **Progress Tracking**: Use progress indicators
   - Total items processed
   - Current item status
   - Estimated time remaining

3. **Memory Management**: Clear cache periodically
   - Keep track of cached prompts
   - Clear unused prompts to free memory

4. **File Organization**: Structure outputs logically
   - Use consistent naming conventions
   - Organize by prompt/speaker
   - Include metadata files

5. **Logging**: Maintain detailed logs
   - Record processing timestamps
   - Log errors and warnings
   - Save final summary

Example logging:
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('processing.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f'Started processing {total_items} items')
""")


if __name__ == "__main__":
    main()
