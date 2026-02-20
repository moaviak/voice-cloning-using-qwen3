# Installation and Setup Guide

## Overview

This guide walks you through installing and setting up the Qwen3-TTS Voice Cloning Engine on your system.

## System Requirements

### Minimum Requirements

- **Python**: 3.10 or higher
- **RAM**: 8 GB minimum (16 GB recommended)
- **Disk Space**: 5 GB for model files + additional space for output audio
- **OS**: Linux, macOS, or Windows

### GPU (Optional but Recommended)

- **GPU Memory**: 8 GB VRAM minimum (16 GB recommended)
- **CUDA**: 11.8 or higher (for NVIDIA GPUs)
- **Supported GPUs**: NVIDIA GPUs with compute capability 8.0+ recommended

## Step-by-Step Installation

### 1. Create a Virtual Environment (Recommended)

It's best to create a isolated Python environment to avoid dependency conflicts.

#### Using venv (Python built-in):

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate          # On Linux/macOS
# or
venv\Scripts\activate              # On Windows
```

#### Using conda:

```bash
# Create environment
conda create -n voice-cloning python=3.10 -y
conda activate voice-cloning
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### 3. Optional: Install GPU Support

#### For NVIDIA GPUs:

```bash
# Install PyTorch with CUDA support
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install Flash Attention (optional, for faster GPU inference)
pip install flash-attn --no-build-isolation
```

**Note**: Flash Attention installation can be challenging. If it fails, the engine will still work without it.

If you have issues installing Flash Attention on your system:

```bash
# Try with limited parallel jobs
MAX_JOBS=2 pip install flash-attn --no-build-isolation

# Or install a precompiled wheel instead (check pytorch lightning)
```

#### For AMD GPUs:

```bash
# Install PyTorch with ROCm support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

#### For CPU Only:

```bash
# CPU version is already included in the base installation
# No additional steps needed, but inference will be slower
```

### 4. Verify Installation

Run the test script to verify everything is installed correctly:

```bash
python test_setup.py
```

This will check:

- ✓ Python version
- ✓ PyTorch installation
- ✓ Required dependencies
- ✓ Model files
- ✓ Engine module
- ✓ GPU/CUDA availability
- ✓ Optional features

### 5. Download/Verify Model Files

The model files should already be in `models/qwen3-tts/`. Verify the required files are present:

```bash
ls -lh models/qwen3-tts/
```

Expected files:

- `config.json` - Model configuration
- `model.safetensors` - Model weights (~3.4 GB)
- `generation_config.json` - Generation parameters
- `preprocessor_config.json` - Preprocessing settings
- `speech_tokenizer/` - Speech tokenizer model

If files are missing, download them using:

```bash
# Using Hugging Face Hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base --local-dir models/qwen3-tts

# Or using ModelScope (faster for mainland China)
pip install -U modelscope
modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-Base --local_dir models/qwen3-tts
```

## Configuration

### Automatic Device Detection (Default)

The engine automatically detects and uses GPU if available, otherwise CPU:

```python
from qwen3_voice_engine import VoiceCloningEngine

engine = VoiceCloningEngine(
    model_path="models/qwen3-tts",
    device=None,  # Auto-detect
)
```

### Manual Device Selection

#### Force GPU:

```python
engine = VoiceCloningEngine(
    model_path="models/qwen3-tts",
    device="cuda:0",
    dtype=torch.bfloat16,
    use_flash_attention=True,  # Optional
)
```

#### Force CPU:

```python
engine = VoiceCloningEngine(
    model_path="models/qwen3-tts",
    device="cpu",
    dtype=torch.float32,
)
```

### Using Configuration Presets

```python
from config import get_config

# High-performance GPU setup
config = get_config("high_performance_gpu")
engine = VoiceCloningEngine(**config.__dict__)

# Low-VRAM GPU setup
config = get_config("low_vram_gpu")
engine = VoiceCloningEngine(**config.__dict__)

# CPU-only setup
config = get_config("cpu")
engine = VoiceCloningEngine(**config.__dict__)
```

## Getting Started

### Quick Start

Run the interactive quickstart:

```bash
python quickstart.py
```

This provides an interactive interface to:

- Initialize the engine
- Create voice prompts
- Synthesize speech
- Manage cached prompts

### Run Examples

View usage examples:

```bash
python examples.py
```

### Real-World Applications

See practical use cases:

```bash
python applications.py
```

## First Use Checklist

After installation, verify everything works:

- [ ] Run `python test_setup.py` - verify all checks pass
- [ ] Run `python quickstart.py` - test the interactive interface
- [ ] Check `examples.py` - understand the API
- [ ] Create sample audio files in `samples/` directory
- [ ] Test voice cloning with your own audio

## Troubleshooting

### CUDA Out of Memory

Error:

```
RuntimeError: CUDA out of memory
```

Solutions:

```python
# Option 1: Use CPU instead
engine = VoiceCloningEngine("models/qwen3-tts", device="cpu")

# Option 2: Use lower precision
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    device="cuda:0",
    dtype=torch.float32
)

# Option 3: Batch smaller texts
for text in texts:
    synthesize(text)  # One at a time instead of batch
```

### CUDA Not Found

Error:

```
RuntimeError: Trying to initialize CUDA but CUDA is not available
```

Solutions:

1. Reinstall PyTorch with CUDA support:

   ```bash
   pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu118
   ```

2. Verify NVIDIA drivers:

   ```bash
   nvidia-smi
   ```

3. Fall back to CPU:
   ```python
   engine = VoiceCloningEngine("models/qwen3-tts", device="cpu")
   ```

### Audio File Issues

Error:

```
ValueError: Failed to load audio
```

Solutions:

- Ensure audio is in WAV format (`.wav`)
- Check file is not corrupted: `ffmpeg -i audio.wav audio_test.wav`
- Verify sample rate is reasonable (8000-48000 Hz)
- Ensure audio duration is at least 3 seconds

### Flash Attention Installation Fails

Solution:

```python
# Engine works fine without Flash Attention
engine = VoiceCloningEngine(
    "models/qwen3-tts",
    use_flash_attention=False  # Disable Flash Attention
)
```

If you still need Flash Attention:

1. Ensure you have CUDA toolkit installed
2. Try building from source:
   ```bash
   git clone https://github.com/Dao-AILab/flash-attention.git
   cd flash-attention
   pip install -e .
   ```

### Import Errors

Error:

```
ImportError: No module named 'qwen_tts'
```

Solution:

```bash
pip install -r requirements.txt
# or
pip install qwen-tts
```

## Environment Variables

You can set environment variables to customize behavior:

```bash
# Limit CUDA memory allocation
export CUDA_VISIBLE_DEVICES=0

# Control memory growth
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Disable CUDA if needed
export CUDA_VISIBLE_DEVICES=

# Run with these set
python quickstart.py
```

## Performance Optimization

### For GPU Users:

1. **Use bfloat16**:

   ```python
   dtype=torch.bfloat16  # Faster and lower memory
   ```

2. **Enable Flash Attention**:

   ```python
   use_flash_attention=True
   ```

3. **Batch Processing**:
   ```python
   # Synthesize multiple texts at once
   texts = [text1, text2, text3, ...]
   wavs, sr = engine.synthesize_voice(text=texts, ...)
   ```

### For CPU Users:

1. **Use Appropriate Precision**:

   ```python
   dtype=torch.float32  # Best for CPU
   ```

2. **Reduce Batch Size**:

   ```python
   # Process one text at a time
   for text in texts:
       engine.synthesize_voice(text=text, ...)
   ```

3. **Allocate Sufficient RAM**:
   - Close other applications
   - Increase swap/page file size if needed

## Next Steps

1. **Read the Main Documentation**: `README.md`
2. **Explore API**: `qwen3_voice_engine.py`
3. **Try Examples**: `examples.py`
4. **See Applications**: `applications.py`
5. **Review Configuration**: `config.py`

## Support

If you encounter issues:

1. Check this installation guide
2. Review `test_setup.py` output for specific errors
3. Check README.md troubleshooting section
4. Review official Qwen3-TTS documentation: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base
5. Open an issue with:
   - Output of `python test_setup.py`
   - Python version
   - OS information
   - Exact error message

## Updating

To update the dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To update specific packages:

```bash
pip install --upgrade torch qwen-tts
```

## Uninstalling

To remove the voice cloning environment:

```bash
# If using venv
deactivate
rm -rf venv

# If using conda
conda deactivate
conda env remove -n voice-cloning
```

To clean up model files (optional, models are ~3.4 GB):

```bash
rm -rf models/qwen3-tts
```
