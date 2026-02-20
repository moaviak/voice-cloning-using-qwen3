# Project Summary: Qwen3-TTS Voice Cloning Engine

## About This Project

This is a complete voice cloning system built on top of the **Qwen3-TTS-12Hz-1.7B-Base** model from Alibaba's Qwen team. The engine enables rapid voice cloning from 3-5 second audio samples and synthesizes new speech with cloned voice characteristics.

## What's Included

### Core Engine

- **qwen3_voice_engine.py** - Main VoiceCloningEngine class with full API
  - Automatic GPU/CPU detection
  - Voice prompt creation from audio + transcript
  - Voice synthesis with multiple language support
  - Batch processing capabilities
  - Prompt caching and memory management

### Configuration & Setup

- **config.py** - Flexible configuration system
  - Preset configurations for different hardware
  - Device and dtype management
  - Hardware-aware configuration recommendations

- **INSTALL.md** - Complete installation guide
  - Step-by-step setup instructions
  - Troubleshooting guide
  - Performance optimization tips
  - GPU/CPU configuration

- **requirements.txt** - Python package dependencies

### Documentation & Examples

- **README.md** - Comprehensive documentation
  - Feature overview
  - API reference
  - Quick start guide
  - Troubleshooting section

- **examples.py** - Usage examples
  - Basic setup
  - Voice cloning workflow
  - Batch synthesis
  - Multilingual synthesis
  - Prompt management
  - Device selection

- **applications.py** - Real-world use cases
  - Audiobook narration
  - Multilingual content
  - Podcast generation
  - Music vocal samples
  - Voice profile management
  - Batch content generation

### Tools & Utilities

- **quickstart.py** - Interactive quickstart script
  - Setup verification
  - Interactive mode for testing
  - Demo mode
  - Hardware detection

- **test_setup.py** - Setup verification tool
  - Python version check
  - PyTorch installation verification
  - Dependencies check
  - Model file verification
  - CUDA/GPU detection
  - Engine initialization test

## Key Features

### ✨ Core Capabilities

- **GPU/CPU Auto-Detection**: Automatically uses GPU if available, falls back to CPU
- **Voice Cloning**: Create reusable voice prompts from reference audio
- **Multi-Language Support**: 10+ languages including Chinese, English, Japanese, Korean, etc.
- **Batch Processing**: Synthesize multiple texts efficiently
- **Prompt Caching**: Reuse voice prompts without recomputation
- **Memory Management**: Cache clearing and efficient resource usage

### 🎯 Use Cases

- Audiobook and podcast narration
- Multilingual content creation
- Music production (vocal samples)
- Customer service voice systems
- Educational content generation
- Content personalization

### 🔧 Technical Features

- PyTorch-based inference
- bfloat16 support for faster GPU inference
- Flash Attention 2 support (optional)
- Flexible device configuration
- Comprehensive error handling
- Logging and debugging support

## Architecture Overview

```
VoiceCloningEngine
├── Model Loading
│   ├── GPU Detection
│   ├── Device Selection
│   └── Model Initialization
├── Voice Prompt Creation
│   ├── Audio Loading
│   ├── Transcript Processing
│   └── Prompt Storage
└── Voice Synthesis
    ├── Text Processing
    ├── Language Detection
    └── Audio Generation
```

## File Structure

```
project/
├── qwen3_voice_engine.py          # Main engine implementation
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── test_setup.py                   # Setup verification
├── quickstart.py                   # Interactive quickstart
├── examples.py                     # Usage examples
├── applications.py                 # Real-world applications
├── README.md                       # Main documentation
├── INSTALL.md                      # Installation guide
├── .gitignore                      # Git ignore rules
└── models/
    └── qwen3-tts/                  # Pre-downloaded model files
        ├── config.json
        ├── model.safetensors
        ├── generation_config.json
        ├── speech_tokenizer/
        └── ...
```

## Getting Started

### 1. Verify Installation

```bash
python test_setup.py
```

### 2. Run Interactive Quickstart

```bash
python quickstart.py
```

### 3. Use the Engine

```python
from qwen3_voice_engine import VoiceCloningEngine
import torch

# Initialize
engine = VoiceCloningEngine("models/qwen3-tts")

# Create voice prompt
prompt = engine.create_voice_clone_prompt(
    audio_path="path/to/reference.wav",
    transcript="Transcription of the reference audio",
    prompt_name="my_voice"
)

# Synthesize speech
audio, sr = engine.synthesize_voice(
    text="New text to synthesize",
    language="English",
    prompt_name=prompt,
    output_path="output/result.wav"
)
```

## Supported Languages

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

## System Requirements

### Minimum

- Python 3.10+
- 8 GB RAM
- 5 GB disk space
- PyTorch 2.0+

### Recommended

- GPU with 8+ GB VRAM
- CUDA Toolkit 11.8+
- 16+ GB system RAM
- SSD storage

## Performance

### Expected Performance

**On GPU (NVIDIA RTX 3080, 10GB VRAM):**

- Inference latency: ~100-200ms per sentence
- Throughput: 5-10 sentences/second
- Memory usage: 4-6 GB VRAM

**On CPU (Intel i7, 32GB RAM):**

- Inference latency: ~2-5 seconds per sentence
- Throughput: 0.2-0.5 sentences/second
- Memory usage: 6-8 GB RAM

## Dependencies

### Core

- torch >= 2.0.0
- transformers
- numpy
- soundfile
- safetensors

### Optional

- flash-attn >= 2.5.0 (for faster GPU inference)

## Troubleshooting

Common issues and solutions:

**CUDA Out of Memory**

- Use CPU instead
- Use float32 instead of bfloat16
- Process smaller batches

**Model Not Found**

- Verify model path: `ls models/qwen3-tts`
- Download model if missing

**Audio Format Issues**

- Ensure WAV format (.wav)
- Duration: 3-5 seconds recommended
- Sample rate: auto-detected

**Flash Attention Installation Fails**

- Optional feature, engine works without it
- Set `use_flash_attention=False`

See README.md and INSTALL.md for more troubleshooting tips.

## API Overview

### Main Methods

**`create_voice_clone_prompt(audio_path, transcript, prompt_name, x_vector_only_mode)`**

- Creates a reusable voice prompt from audio and transcript
- Returns: prompt identifier string

**`synthesize_voice(text, language, prompt_name, output_path)`**

- Synthesizes speech with cloned voice
- Returns: (audio_array, sample_rate)

**`synthesize_and_save(text, output_path, language, prompt_name)`**

- Shorthand for synthesizing and saving to file
- Returns: output path

**`list_cached_prompts()`**

- Lists all cached voice prompts
- Returns: list of prompt names

**`clear_prompt_cache(prompt_name)`**

- Clears cached prompts to free memory
- If prompt_name is None, clears all

## Configuration Presets

Choose from preconfigured setups:

- **high_performance_gpu** - Best for high-VRAM GPUs (16GB+)
- **standard_gpu** - Balanced GPU setup (8GB+ VRAM)
- **low_vram_gpu** - For GPUs with <8GB VRAM
- **cpu** - CPU-only inference
- **auto** - Automatic hardware detection (default)

## Data Type Options

- **torch.bfloat16** - Faster GPU, lower precision
- **torch.float32** - Better CPU compatibility, slower GPU

## Model Information

**Qwen3-TTS-12Hz-1.7B-Base**

- Parameters: 1.7 billion
- Sample Rate: 24 kHz
- Languages: 10+ languages
- Architecture: Discrete multi-codebook LM
- Features: Voice cloning, streaming generation

## References

- [Qwen3-TTS HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base)
- [GitHub Repository](https://github.com/QwenLM/Qwen3-TTS)
- [Technical Paper](https://arxiv.org/abs/2601.15621)

## Citation

If you use this project, cite:

```bibtex
@article{Qwen3-TTS,
  title={Qwen3-TTS Technical Report},
  author={Hangrui Hu and others},
  journal={arXiv preprint arXiv:2601.15621},
  year={2026}
}
```

## License

Qwen3-TTS is released under Apache License 2.0.

## Next Steps

1. **Install**: Follow INSTALL.md
2. **Verify**: Run test_setup.py
3. **Test**: Use quickstart.py
4. **Learn**: Read README.md
5. **Explore**: Check examples.py and applications.py
6. **Implement**: Use the engine in your projects

## Support & Issues

For help:

1. Check README.md Troubleshooting
2. Review INSTALL.md Installation Guide
3. Check example code in examples.py
4. See real-world applications in applications.py
5. Review docstrings in qwen3_voice_engine.py

## Version History

- **v1.0.0** - Initial release
  - Core VoiceCloningEngine implementation
  - GPU/CPU auto-detection
  - Complete documentation
  - Setup verification tools
  - Example codes and applications

## Contributors

- Built with Qwen3-TTS from Alibaba Qwen team
- Wraps qwen-tts Python package

## Acknowledgments

- Alibaba Qwen team for the Qwen3-TTS model
- PyTorch team for the core tensor framework
- HuggingFace for model hosting
