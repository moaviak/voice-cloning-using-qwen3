# Project Structure Guide

## Overview

The Voice Cloning project is organized as a modular Python package with clear separation of concerns. This document explains the directory structure and how to navigate the codebase.

## Directory Structure

```
voice-cloning-using-qwen3/
│
├── src/                              # Main source code directory
│   └── voice_cloning/               # Main package
│       ├── __init__.py              # Package initialization
│       │
│       ├── core/                    # Core engine module
│       │   └── __init__.py          # VoiceCloningEngine class
│       │
│       ├── config/                  # Configuration module
│       │   └── __init__.py          # EngineConfig and presets
│       │
│       ├── api/                     # FastAPI application
│       │   ├── __init__.py          # Package exports
│       │   ├── main.py              # FastAPI app factory
│       │   │
│       │   ├── routes/              # API endpoints
│       │   │   ├── __init__.py
│       │   │   ├── health.py        # Health check endpoints
│       │   │   ├── synthesis.py     # Create prompt & synthesize
│       │   │   └── management.py    # Prompt management
│       │   │
│       │   ├── models/              # Pydantic request/response models
│       │   │   └── __init__.py      # Request and response schemas
│       │   │
│       │   └── utils/               # API utilities
│       │       └── __init__.py      # Helper functions
│       │
│       └── utils/                   # Shared utilities
│           └── __init__.py          # General helpers
│
├── tests/                           # Test directory
│   ├── __init__.py
│   ├── test_engine.py              # Engine tests
│   ├── test_config.py              # Configuration tests
│   ├── test_api.py                 # API endpoint tests
│   └── fixtures/                    # Test fixtures and mocks
│
├── examples/                        # Usage examples
│   ├── basic_examples.py           # Basic engine usage
│   ├── api_examples.py             # REST API examples
│   ├── applications.py             # Real-world applications
│   └── quickstart.py               # Quick start guide
│
├── scripts/                         # CLI scripts and runners
│   ├── run_api.py                  # Start FastAPI server
│   └── cli.py                      # CLI interface (future)
│
├── notebooks/                       # Jupyter notebooks
│   └── test.ipynb                  # Testing notebook for Colab
│
├── models/                          # Model files (gitignored)
│   └── qwen3-tts/                  # Model directory
│       ├── config.json
│       ├── model.safetensors
│       └── ...
│
├── docs/                            # Documentation
│   ├── README.md                    # Main documentation
│   ├── INSTALL.md                   # Installation guide
│   ├── API.md                       # REST API documentation
│   ├── PROJECT_SUMMARY.md           # Project overview
│   └── INDEX.md                     # Navigation guide
│
├── config/                          # Configuration files
│   └── .env.example                 # Example environment file
│
├── setup.py                         # Package setup and installation
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # Repository README
```

## Module Descriptions

### Core Engine (`src/voice_cloning/core/`)

The core voice cloning functionality:

- **VoiceCloningEngine**: Main class for voice cloning operations
- Features:
  - GPU/CPU auto-detection
  - Model loading from local path
  - Voice prompt creation from audio + transcription
  - Voice synthesis/TTS with cloning
  - Prompt caching

**Key Classes:**

- `VoiceCloningEngine` - Main engine class

**Usage:**

```python
from voice_cloning.core import VoiceCloningEngine

engine = VoiceCloningEngine(
    model_path="path/to/model",
    device="cuda:0",
    dtype=torch.bfloat16
)
```

### Configuration (`src/voice_cloning/config/`)

Hardware detection and configuration management:

- **EngineConfig**: Dataclass with all configuration options
- **Presets**: Pre-configured hardware profiles
  - `high_performance_gpu` - For high-end GPUs
  - `standard_gpu` - For typical GPUs
  - `low_vram_gpu` - For GPUs with < 8GB VRAM
  - `cpu` - CPU-only mode
  - `auto` - Auto-detect hardware

**Key Functions:**

- `get_recommended_config_for_hardware()` - Auto-detect optimal config
- `get_config(preset)` - Get preset configuration

**Usage:**

```python
from voice_cloning.config import get_recommended_config_for_hardware

config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(
    model_path=config.model_path,
    device=config.device,
    dtype=config.dtype
)
```

### FastAPI Application (`src/voice_cloning/api/`)

REST API for voice cloning:

- **main.py**: FastAPI application factory
- **routes/**: Endpoint definitions
  - `health.py`: Health checks, status
  - `synthesis.py`: Create prompts, synthesize audio
  - `management.py`: Manage cached prompts
- **models/**: Pydantic request/response schemas
- **utils/**: Helper functions

**Endpoints:**

- `GET /api/v1/health` - Health check
- `POST /api/v1/create-prompt` - Create voice prompt
- `POST /api/v1/synthesize` - Synthesize voice
- `GET /api/v1/download/{filename}` - Download audio
- `GET /api/v1/prompts` - List prompts
- `DELETE /api/v1/prompts/{id}` - Delete prompt

**Usage:**

```python
from voice_cloning.api import app

# Run with: uvicorn voice_cloning.api:app --reload
```

### Examples (`examples/`)

Usage examples for different scenarios:

- **basic_examples.py** - Engine usage examples
- **api_examples.py** - REST API examples
- **applications.py** - Real-world use cases
- **quickstart.py** - Quick start tutorial

## Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/voice-cloning
cd voice-cloning
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Package (Development)

```bash
pip install -e .
```

Or install requirements directly:

```bash
pip install -r requirements.txt
```

### 4. Download Model

Place the Qwen3-TTS model in `models/qwen3-tts/`

## Running the Code

### Using the Engine Directly

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# Get optimal config for your hardware
config = get_recommended_config_for_hardware()

# Initialize engine
engine = VoiceCloningEngine(
    model_path="models/qwen3-tts",
    device=config.device,
    dtype=config.dtype
)

# Create voice prompt
engine.create_voice_clone_prompt(
    audio_path="reference.wav",
    transcript="Your voice sample text"
)

# Synthesize speech
audio, sr = engine.synthesize_voice(
    text="Hello world",
    language="English",
    prompt_name="my_voice"
)
```

### Using the REST API

```bash
# Start the API server
python scripts/run_api.py --port 8000

# In another terminal, make requests
curl -X POST http://localhost:8000/api/v1/create-prompt \
  -F "audio=@reference.wav" \
  -F "transcript=Your text"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_engine.py

# With verbose output
pytest -v

# With coverage
pytest --cov=src/voice_cloning
```

### Running Examples

```bash
# Basic examples
python examples/basic_examples.py

# API examples (requires running API server)
python examples/api_examples.py

# Quickstart
python examples/quickstart.py
```

## Development Guidelines

### Code Organization

1. **Core Logic**: Keep in `src/voice_cloning/core/`
2. **Configuration**: Use `src/voice_cloning/config/`
3. **API Endpoints**: Add to appropriate file in `src/voice_cloning/api/routes/`
4. **Models/Schemas**: Add to `src/voice_cloning/api/models/`
5. **Tests**: Mirror structure in `tests/`

### Adding New Features

1. **New Engine Feature**:
   - Add method to `VoiceCloningEngine` in `src/voice_cloning/core/`
   - Add tests in `tests/test_engine.py`

2. **New API Endpoint**:
   - Add route handler to appropriate file in `src/voice_cloning/api/routes/`
   - Add Pydantic model in `src/voice_cloning/api/models/`
   - Add tests in `tests/test_api.py`
   - Register route in `src/voice_cloning/api/main.py`

3. **New Configuration Option**:
   - Add field to `EngineConfig` dataclass in `src/voice_cloning/config/`
   - Update validation and documentation

### Code Style

Follow PEP 8 with these tools:

```bash
# Format code
black src/ tests/ examples/

# Check style
flake8 src/ tests/ examples/

# Type checking (future)
mypy src/
```

## Common Tasks

### Create Voice Prompt

```python
prompt_name = engine.create_voice_clone_prompt(
    audio_path="path/to/audio.wav",
    transcript="Text transcription of audio",
    prompt_name="optional_custom_name"
)
```

### Synthesize Speech

```python
# Single synthesis
audio, sr = engine.synthesize_voice(
    text="Text to synthesize",
    language="English",
    prompt_name=prompt_name,
    output_path="output.wav"
)

# Batch synthesis
texts = ["Text 1", "Text 2", "Text 3"]
wavs, sr = engine.synthesize_voice(
    text=texts,
    language="English",
    prompt_name=prompt_name
)
```

### Manage Prompts

```python
# List all prompts
prompts = engine.list_cached_prompts()

# Get supported languages
languages = engine.get_supported_languages()

# Clear specific prompt
engine.clear_prompt_cache("prompt_name")

# Clear all prompts
engine.clear_prompt_cache()
```

## Project Structure Benefits

✅ **Modularity** - Clear separation of concerns
✅ **Scalability** - Easy to add new features
✅ **Testability** - Easy to write and run tests
✅ **Maintainability** - Clear code organization
✅ **Documentation** - Consistent docstrings and examples
✅ **Packaging** - Proper Python package structure
✅ **Installation** - Install as package with `pip install -e .`

## File Locations Reference

| Purpose         | Location                               |
| --------------- | -------------------------------------- |
| Core Engine     | `src/voice_cloning/core/__init__.py`   |
| Configuration   | `src/voice_cloning/config/__init__.py` |
| API Application | `src/voice_cloning/api/main.py`        |
| API Routes      | `src/voice_cloning/api/routes/`        |
| Run API         | `scripts/run_api.py`                   |
| Basic Examples  | `examples/basic_examples.py`           |
| API Examples    | `examples/api_examples.py`             |
| Tests           | `tests/`                               |
| Documentation   | `docs/`                                |
| Model Files     | `models/qwen3-tts/`                    |

## Support and Documentation

- 📚 **Main README**: `README.md`
- 📖 **Installation**: `docs/INSTALL.md`
- 🔌 **API Docs**: `docs/API.md`
- 📋 **Project Summary**: `docs/PROJECT_SUMMARY.md`
- 🗺️ **Navigation**: `docs/INDEX.md`
- 💻 **Examples**: `examples/`
- 🧪 **Tests**: `tests/`
