# Qwen3-TTS Voice Cloning Engine

A Python-based voice cloning system built on Qwen3-TTS-12Hz-1.7B-Base model. This engine enables rapid voice cloning from 3-5 second audio samples and synthesizes new speech with the cloned voice.

## Features

✨ **Key Capabilities:**

- **GPU/CPU Auto-Detection**: Automatically detects and uses GPU if available, falls back to CPU
- **Voice Cloning**: Create reusable voice prompts from reference audio + transcript
- **Voice Synthesis**: Generate new speech with cloned voice characteristics
- **Batch Processing**: Synthesize multiple texts in a single operation
- **Multilingual Support**: Supports 10+ languages with auto-language detection
- **Cached Prompts**: Reuse voice prompts without recomputing features
- **Efficient Memory Management**: Cache clearing and prompt management

## Installation

### Prerequisites

- Python 3.10+
- PyTorch 2.0+
- CUDA Toolkit 11.8+ (optional, for GPU acceleration)

### Setup Steps

1. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Optional: Install Flash Attention for faster GPU inference**:

```bash
pip install flash-attn --no-build-isolation
```

Note: Flash Attention requires CUDA-compatible GPU and may need to be built on your system. If installation fails, the engine will still work without it.

4. **Download the Qwen3-TTS model (recommended)**:

Use the provided helper script to download `Qwen/Qwen3-TTS-12Hz-1.7B-Base` into `models/qwen3-tts`:

```bash
python scripts/download_model.py
```

After this completes successfully, the engine and API will load the model from `models/qwen-3tts` without needing to fetch weights at runtime.

## Quick Start

### Basic Usage (Engine Only)

```python
from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# Initialize engine (auto-detects GPU/CPU and dtype)
config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(config)

# Step 1: Create a voice prompt from reference audio
# This returns an internal prompt object and also caches it under "my_voice".
voice_clone_prompt = engine.create_voice_clone_prompt(
    audio_path="path/to/reference.wav",
    transcript="The transcribed text of the reference audio",
    prompt_name="my_voice",
)

# Step 2: Synthesize new speech with the cloned voice
audio, sample_rate = engine.synthesize_voice(
    text="This is new speech synthesized with the cloned voice!",
    language="English",
    voice_clone_prompt=voice_clone_prompt,  # preferred for stateless usage
    prompt_name="my_voice",                 # optional, uses cache if available
    output_path="output/cloned_speech.wav",
)
```

## API Reference

### VoiceCloningEngine

Main class for voice cloning and synthesis operations.

#### Initialization

```python
engine = VoiceCloningEngine(
    model_path: Union[str, Path] | EngineConfig,
    device: Optional[str] = None,
    dtype: torch.dtype = torch.bfloat16,
    use_flash_attention: bool = False,
)
```

**Parameters:**

- `model_path`: Path to the Qwen3-TTS model directory (required)
- `device`: Device to use ('cuda:0', 'cpu', or None for auto-detection)
- `dtype`: Data type for inference (torch.bfloat16 or torch.float32)
  - Use `torch.bfloat16` for faster GPU inference (default)
  - Use `torch.float32` for CPU inference for better compatibility
- `use_flash_attention`: Enable Flash Attention 2 for GPU (requires compatible GPU)

**Example:**

```python
# Auto-detect GPU/CPU
engine = VoiceCloningEngine("models/qwen3-tts")

# Force GPU with Flash Attention
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    device="cuda:0",
    dtype=torch.bfloat16,
    use_flash_attention=True
)

# Force CPU
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    device="cpu",
    dtype=torch.float32
)
```

#### Methods

##### `create_voice_clone_prompt()`

Create a reusable voice prompt from audio file and transcript.

```python
voice_clone_prompt = engine.create_voice_clone_prompt(
    audio_path: Union[str, Path],
    transcript: str,
    prompt_name: Optional[str] = None,
    x_vector_only_mode: bool = False,
)
```

**Parameters:**

- `audio_path`: Path to reference audio (.wav file, ideally 3-5 seconds)
- `transcript`: Text content corresponding to the audio
- `prompt_name`: Name to identify this prompt (auto-generated if not provided)
- `x_vector_only_mode`:
  - `False` (default): Best quality, uses both speaker and content information
  - `True`: Faster but lower quality, uses only speaker embedding

**Returns:** Internal prompt object (can be passed directly to `synthesize_voice` via `voice_clone_prompt`) and is also cached under `prompt_name` if provided.

**Example:**

```python
voice_clone_prompt = engine.create_voice_clone_prompt(
    audio_path="samples/john_voice.wav",
    transcript="Hello, my name is John.",
    prompt_name="john",
    x_vector_only_mode=False,
)
```

##### `synthesize_voice()`

Synthesize speech using a voice clone prompt.

```python
audio, sample_rate = engine.synthesize_voice(
    text: Union[str, List[str]],
    language: Union[str, List[str]] = "Auto",
    prompt_name: Optional[str] = None,
    voice_clone_prompt: Optional[Any] = None,
    output_path: Optional[Union[str, Path]] = None
) -> Tuple[np.ndarray, int]
```

**Parameters:**

- `text`: Text to synthesize (single string or list for batch)
- `language`: Language code (see Supported Languages below)
  - "Auto" for automatic language detection
- `prompt_name`: Name of cached prompt to use
- `voice_clone_prompt`: Direct prompt object (alternative to prompt_name)
- `output_path`: Optional file path to save output audio

**Returns:** Tuple of (audio_array, sample_rate)

**Example:**

```python
# Single synthesis
audio, sr = engine.synthesize_voice(
    text="Hello, world!",
    language="English",
    prompt_name="john",
    output_path="output/hello.wav"
)

# Batch synthesis
texts = ["First sentence.", "Second sentence.", "Third sentence."]
wavs, sr = engine.synthesize_voice(
    text=texts,
    language="English",
    prompt_name="john",
    output_path="output/batch/"  # Creates output_0.wav, output_1.wav, etc.
)
```

##### `synthesize_and_save()`

Shorthand for synthesizing and saving to file.

```python
output_path = engine.synthesize_and_save(
    text: Union[str, List[str]],
    output_path: Union[str, Path],
    language: Union[str, List[str]] = "Auto",
    prompt_name: Optional[str] = None,
    voice_clone_prompt: Optional[Any] = None
) -> Path
```

##### `list_cached_prompts()`

Get all cached voice prompts.

```python
prompts = engine.list_cached_prompts() -> List[str]
```

**Example:**

```python
prompts = engine.list_cached_prompts()
# Returns: ["john", "mary", "bob"]
```

##### `clear_prompt_cache()`

Clear cached prompts to free memory.

```python
engine.clear_prompt_cache(prompt_name: Optional[str] = None) -> None
```

**Parameters:**

- `prompt_name`: Specific prompt to clear. If None, clears all.

**Example:**

```python
# Clear specific prompt
engine.clear_prompt_cache("john")

# Clear all prompts
engine.clear_prompt_cache()
```

##### `get_supported_languages()`

Get list of supported languages.

```python
languages = engine.get_supported_languages() -> List[str]
```

## Supported Languages

The engine supports the following languages:

- Auto (automatic detection)
- Chinese
- English
- Japanese
- Korean
- German
- French
- Russian
- Portuguese
- Spanish
- Italian

## Device Configuration

### Auto-Detection (Recommended)

```python
engine = VoiceCloningEngine("models/qwen3-tts", device=None)
```

The engine automatically uses GPU if available, otherwise CPU.

### GPU Usage

```python
import torch
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    device="cuda:0",
    dtype=torch.bfloat16,  # Better performance
    use_flash_attention=True  # If installed
)
```

### CPU Usage

```python
import torch
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    device="cpu",
    dtype=torch.float32  # Better compatibility on CPU
)
```

## Data Type Selection

**torch.bfloat16** (Recommended for GPU):

- Faster inference
- Lower memory usage
- Slightly lower precision
- Only works on GPU
- Requires GPU with bfloat16 support

**torch.float32**:

- Better compatibility
- Slower inference
- Higher memory usage
- Works on both GPU and CPU

## Examples

### Example 1: Basic Voice Cloning

```python
from qwen3_voice_engine import VoiceCloningEngine
import torch

# Initialize
engine = VoiceCloningEngine("models/qwen3-tts")

# Create prompt
prompt = engine.create_voice_clone_prompt(
    audio_path="recordings/sample.wav",
    transcript="This is a sample recording"
)

# Synthesize new speech
audio, sr = engine.synthesize_voice(
    text="Hello, this is synthesized speech!",
    language="English",
    prompt_name=prompt,
    output_path="output/result.wav"
)
```

### Example 2: Batch Processing

```python
texts = [
    "First sentence to synthesize.",
    "Second sentence to synthesize.",
    "Third sentence to synthesize.",
]

wavs, sr = engine.synthesize_voice(
    text=texts,
    language="English",
    prompt_name=prompt,
    output_path="output/batch/"
)
# Generates: output_0.wav, output_1.wav, output_2.wav
```

### Example 3: Multilingual Synthesis

```python
languages_and_texts = {
    "English": "This is in English",
    "Chinese": "这是中文",
    "Spanish": "Esto es en español",
}

for language, text in languages_and_texts.items():
    audio, sr = engine.synthesize_voice(
        text=text,
        language=language,
        prompt_name=prompt,
        output_path=f"output/{language.lower()}.wav"
    )
```

### Example 4: Multiple Voice Prompts

```python
# Create multiple voice prompts
voices = {}
voices["male"] = engine.create_voice_clone_prompt(
    audio_path="voices/male.wav",
    transcript="Male voice recording",
    prompt_name="male"
)

voices["female"] = engine.create_voice_clone_prompt(
    audio_path="voices/female.wav",
    transcript="Female voice recording",
    prompt_name="female"
)

# Use each voice for different texts
male_audio, sr = engine.synthesize_voice(
    text="Deep male voice",
    prompt_name="male",
    output_path="output/male.wav"
)

female_audio, sr = engine.synthesize_voice(
    text="Bright female voice",
    prompt_name="female",
    output_path="output/female.wav"
)

# List all voices
print(engine.list_cached_prompts())  # ["male", "female"]
```

## Troubleshooting

### CUDA Out of Memory (OOM)

**Error:** `RuntimeError: CUDA out of memory`

**Solutions:**

1. Use CPU instead:

   ```python
   engine = VoiceCloningEngine("models/qwen3-tts", device="cpu")
   ```

2. Use float32 instead of bfloat16:

   ```python
   engine = VoiceCloningEngine(
       "models/qwen3-tts",
       dtype=torch.float32
   )
   ```

3. Process in smaller batches

### Model Not Found

**Error:** `FileNotFoundError: Model path not found`

**Solution:** Verify the model path:

```python
from pathlib import Path
model_path = Path("models/qwen3-tts")
assert model_path.exists(), f"Model not found at {model_path.absolute()}"
```

### Audio Format Issues

**Error:** `ValueError: Failed to load audio`

**Solution:** Ensure audio is:

- WAV format (.wav)
- Mono or stereo
- Sample rate will be auto-detected
- Duration: 3-5 seconds recommended for best results

### Flash Attention Installation Failed

If `flash-attn` installation fails, the engine will work without it. Simply set `use_flash_attention=False` in the initialization.

## Performance Tips

### For GPU Users

1. Use `torch.bfloat16` for faster inference
2. Enable Flash Attention if available (requires CUDA)
3. Batch multiple texts together
4. Cache prompts to avoid recomputation

### For CPU Users

1. Use `torch.float32` for better compatibility
2. Be patient - inference will be slower
3. Ensure sufficient RAM (model requires ~4GB+)
4. Process shorter texts for better performance

### General Tips

1. Provide high-quality reference audio (clear, minimal noise)
2. Use accurate transcripts for reference audio
3. Clear unused prompts from cache to free memory
4. Use "Auto" language detection when unsure of language

## Model Information

**Model**: Qwen3-TTS-12Hz-1.7B-Base

- **Parameters**: 1.7 billion
- **Sample Rate**: 24000 Hz (24 kHz)
- **Supported Languages**: 10+ languages
- **Audio Duration**: 3+ seconds recommended for voice cloning
- **Architecture**: Discrete multi-codebook language model
- **Features**: Voice cloning, streaming generation, text-to-speech

## File Structure

```
project/
├── qwen3_voice_engine.py      # Main engine implementation
├── examples.py                # Usage examples
├── requirements.txt           # Python dependencies
├── models/qwen3-tts/          # Model directory (your model files)
│   ├── config.json
│   ├── model.safetensors
│   ├── generation_config.json
│   └── ...
└── output/                    # Generated audio files (created automatically)
    └── *.wav
```

## License

This implementation wraps the Qwen3-TTS model which is licensed under Apache 2.0.

## References

- [Qwen3-TTS HuggingFace Hub](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base)
- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS Technical Report](https://arxiv.org/abs/2601.15621)

## Citation

If you use this engine in your research, please cite:

```bibtex
@article{Qwen3-TTS,
  title={Qwen3-TTS Technical Report},
  author={Hangrui Hu and others},
  journal={arXiv preprint arXiv:2601.15621},
  year={2026}
}
```

## Support

For issues and questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the examples in `examples.py`
3. Check the docstrings in `qwen3_voice_engine.py`
4. Refer to the [Qwen3-TTS documentation](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base)
