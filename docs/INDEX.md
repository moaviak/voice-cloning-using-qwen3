# Quick Navigation Guide

## 📚 Documentation Files

Start here based on what you need:

### For First-Time Setup

1. **[INSTALL.md](INSTALL.md)** - Complete installation guide
   - System requirements
   - Step-by-step installation
   - GPU/CPU setup
   - Troubleshooting

2. **[test_setup.py](test_setup.py)** - Verify your installation
   - Run: `python test_setup.py`
   - Checks Python, PyTorch, dependencies, GPU, model files

### For Learning the API

1. **[README.md](README.md)** - Main documentation (START HERE)
   - Feature overview
   - Quick start code
   - Complete API reference
   - All supported languages
   - Troubleshooting guide

2. **[qwen3_voice_engine.py](qwen3_voice_engine.py)** - Source code with docstrings
   - Full implementation
   - Detailed docstrings for each method
   - Usage examples in docstrings

### For Code Examples

1. **[examples.py](examples.py)** - 6 usage examples
   - Basic setup
   - Voice cloning
   - Batch synthesis
   - Multilingual support
   - Prompt management
   - Device selection

2. **[applications.py](applications.py)** - Real-world use cases
   - Audiobook narration
   - Multilingual content
   - Podcast generation
   - Music production
   - Voice profile management
   - Batch processing

3. **[quickstart.py](quickstart.py)** - Interactive demo
   - Run: `python quickstart.py`
   - Interactive testing
   - Hardware detection
   - Demo mode

### For Configuration

1. **[config.py](config.py)** - Configuration system
   - Hardware detection
   - Device presets
   - Configuration validation
   - Recommended settings

2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
   - What's included
   - Architecture
   - Getting started
   - Reference information

## 🚀 Quick Start (3 Steps)

### Step 1: Install

```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python test_setup.py
```

### Step 2: Learn

```python
# Run interactive demo
python quickstart.py

# Or read examples
python examples.py
```

### Step 3: Use

```python
from qwen3_voice_engine import VoiceCloningEngine

engine = VoiceCloningEngine("models/qwen3-tts")

# Create voice prompt from reference audio
prompt = engine.create_voice_clone_prompt(
    audio_path="path/to/audio.wav",
    transcript="Text matching the audio",
    prompt_name="my_voice"
)

# Synthesize new speech
audio, sr = engine.synthesize_voice(
    text="New text to synthesize",
    language="English",
    prompt_name=prompt,
    output_path="output/result.wav"
)
```

## 📖 Complete Documentation Index

### Installation & Setup

- [INSTALL.md](INSTALL.md) - Installation guide with troubleshooting
- [test_setup.py](test_setup.py) - Verification script
- [requirements.txt](requirements.txt) - Python package dependencies
- [config.py](config.py) - Configuration and presets

### Main Documentation

- [README.md](README.md) - **START HERE** - Complete guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- [INDEX.md](INDEX.md) - This file

### Code & Examples

- [qwen3_voice_engine.py](qwen3_voice_engine.py) - Main engine implementation
- [examples.py](examples.py) - 6 basic usage examples
- [applications.py](applications.py) - 6 real-world use cases
- [quickstart.py](quickstart.py) - Interactive demo script

### Configuration Files

- [.gitignore](.gitignore) - Git ignore patterns
- [models/qwen3-tts/](models/qwen3-tts/) - Pre-downloaded model files

## 🎯 How to Use This Documentation

### I'm New to This Project

1. Read [README.md](README.md) - Overview and quick start
2. Run `python test_setup.py` - Verify installation
3. Run `python quickstart.py` - Try interactive demo
4. Check [examples.py](examples.py) - See basic usage

### I Want to Use the Engine

1. Check [README.md](README.md) - API Reference section
2. Review [examples.py](examples.py) - Find similar examples
3. Check [config.py](config.py) - See configuration options
4. Copy code and adapt to your needs

### I Have an Issue

1. Check [README.md](README.md) - Troubleshooting section
2. Check [INSTALL.md](INSTALL.md) - Installation troubleshooting
3. Run `python test_setup.py` - Identify specific issue
4. Review error message in corresponding documentation

### I Want Real-World Examples

1. See [applications.py](applications.py) - 6 industry use cases
2. Review [README.md](README.md) - Examples section
3. Check [examples.py](examples.py) - Coding patterns

### I Need Hardware Optimization

1. Read [INSTALL.md](INSTALL.md) - GPU/CPU setup
2. Check [config.py](config.py) - Hardware presets
3. See [README.md](README.md) - Performance tips
4. Review [examples.py](examples.py) - Device selection example

## 📋 Feature Overview

### Core Features

- ✅ GPU/CPU auto-detection
- ✅ Voice cloning from audio + transcript
- ✅ Batch text synthesis
- ✅ 10+ language support
- ✅ Prompt caching
- ✅ Memory management
- ✅ Easy-to-use API

### Supported Operations

**Creating Voice Prompts**

```python
prompt = engine.create_voice_clone_prompt(
    audio_path="sample.wav",
    transcript="Sample text",
    prompt_name="my_voice"
)
```

**Synthesizing Speech**

```python
audio, sr = engine.synthesize_voice(
    text="Text to synthesize",
    language="English",
    prompt_name=prompt,
    output_path="output/result.wav"
)
```

**Managing Prompts**

```python
engine.list_cached_prompts()        # List all prompts
engine.clear_prompt_cache()          # Clear all prompts
engine.get_supported_languages()     # Show languages
```

## 🔧 File Descriptions

| File                  | Purpose              | Type          |
| --------------------- | -------------------- | ------------- |
| README.md             | Main documentation   | Documentation |
| INSTALL.md            | Installation guide   | Documentation |
| PROJECT_SUMMARY.md    | Project overview     | Documentation |
| INDEX.md              | This file            | Documentation |
| qwen3_voice_engine.py | Main engine          | Python Code   |
| config.py             | Configuration system | Python Code   |
| examples.py           | Usage examples       | Python Code   |
| applications.py       | Real-world use cases | Python Code   |
| quickstart.py         | Interactive demo     | Python Code   |
| test_setup.py         | Setup verification   | Python Code   |
| requirements.txt      | Dependencies         | Configuration |
| .gitignore            | Git ignore rules     | Configuration |

## 🎓 Learning Path

### 1. Beginner

- Read: README.md (Quick Start section)
- Do: `python test_setup.py`
- Do: `python quickstart.py`
- Read: examples.py

### 2. Intermediate

- Read: README.md (API Reference section)
- Review: qwen3_voice_engine.py docstrings
- Study: applications.py use cases
- Experiment: Modify examples.py code

### 3. Advanced

- Read: PROJECT_SUMMARY.md (Architecture section)
- Review: qwen3_voice_engine.py implementation
- Study: config.py configuration system
- Optimize: Use config.py presets for your hardware

### 4. Expert

- Understand: Qwen3-TTS model architecture
- Extend: Subclass VoiceCloningEngine
- Integrate: Use in production applications
- Optimize: Fine-tune for specific use cases

## 💡 Common Tasks

### Set Up for the First Time

```bash
pip install -r requirements.txt
python test_setup.py
python quickstart.py
```

### Clone a Voice

```python
from qwen3_voice_engine import VoiceCloningEngine
engine = VoiceCloningEngine("models/qwen3-tts")
prompt = engine.create_voice_clone_prompt("audio.wav", "transcript")
audio, sr = engine.synthesize_voice("text", prompt_name=prompt)
```

### Use GPU with Best Performance

```python
from config import get_config
config = get_config("high_performance_gpu")
engine = VoiceCloningEngine(**config.__dict__)
```

### Process Multiple Texts

```python
texts = ["Text 1", "Text 2", "Text 3"]
wavs, sr = engine.synthesize_voice(
    text=texts,
    language="English",
    prompt_name=prompt_name
)
```

### Multi-Language Support

```python
languages = ["English", "Chinese", "Spanish"]
texts = ["English text", "中文文本", "Texto español"]
wavs, sr = engine.synthesize_voice(
    text=texts,
    language=languages,
    prompt_name=prompt_name
)
```

## 🆘 Getting Help

### Check Documentation In This Order:

1. **README.md** - Comprehensive guide and troubleshooting
2. **INSTALL.md** - Installation-specific help
3. **PROJECT_SUMMARY.md** - Architecture and reference
4. **Code docstrings** - In qwen3_voice_engine.py

### Run Verification Tools:

```bash
python test_setup.py      # Check system setup
python quickstart.py      # Test interactively
python examples.py        # See example code
python applications.py    # See real-world usage
```

### If You Find Issues:

1. Note the exact error message
2. Run `python test_setup.py` and check output
3. Search relevant documentation file
4. Review appropriate example in examples.py
5. Check Reddit/GitHub issues (Qwen3-TTS repo)

## 📞 Support Resources

### Included in Project

- Complete documentation (README.md)
- Installation guide (INSTALL.md)
- Code examples (examples.py, applications.py)
- Setup verification (test_setup.py)
- Configuration guide (config.py)

### External Resources

- [Qwen3-TTS HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base)
- [GitHub Repository](https://github.com/QwenLM/Qwen3-TTS)
- [Technical Paper](https://arxiv.org/abs/2601.15621)

## ✅ Checklist for New Users

- [ ] Read README.md quick start
- [ ] Run `python test_setup.py`
- [ ] Run `python quickstart.py`
- [ ] Review examples.py
- [ ] Create test samples directory
- [ ] Try cloning a voice
- [ ] Explore different languages
- [ ] Check configuration options
- [ ] Review production use cases in applications.py

---

**Last Updated**: 2026-02-17  
**Version**: 1.0.0  
**Qwen3-TTS Model**: Base-12Hz-1.7B

For the most up-to-date information, refer to the official Qwen3-TTS repository.
