# Quick Start Guide

Get started with the Voice Cloning system in 5 minutes.

## Installation

```bash
# Option 1: Direct from source
pip install -r requirements.txt

# Option 2: As a package (recommended for development)
pip install -e .
```

## Verify Installation

```bash
# Test that everything is installed
python -c "from voice_cloning import VoiceCloningEngine; print('✓ Installation OK')"
```

## 5-Minute Quickstart

### 1. **Using the Engine Directly**

```python
from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# Initialize
config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(config)

# Create voice clone from audio + transcript and keep the prompt object
voice_clone_prompt = engine.create_voice_clone_prompt(
    audio_path="voice.wav",
    transcript="Hello, this is my voice.",
    prompt_name="my_voice",
)

# Synthesize text with the cloned voice using the prompt object
audio, sample_rate = engine.synthesize_voice(
    text="Some new text to speak",
    language="English",
    voice_clone_prompt=voice_clone_prompt,
    prompt_name="my_voice",
)

# Save output
import soundfile as sf

sf.write("output.wav", audio, sample_rate)
```

### 2. **Using the REST API**

**Start the server:**

```bash
python scripts/run_api.py --port 8000
# Server now running at http://localhost:8000
```

**Use the API (stateless prompt usage):**

```python
import requests

# Create voice clone and get serialized prompt object back
resp = requests.post(
    "http://localhost:8000/api/v1/create-prompt",
    files={"audio": open("voice.wav", "rb")},
    data={
        "transcript": "Hello, this is my voice.",
        "prompt_name": "my_voice",
        "language": "English",
    },
)
resp.raise_for_status()
data = resp.json()
voice_clone_prompt = data["voice_clone_prompt"]  # base64-encoded prompt

# Synthesize audio by sending the serialized prompt (no server-side cache needed)
resp = requests.post(
    "http://localhost:8000/api/v1/synthesize",
    json={
        "text": "Some new text",
        "language": "English",
        "voice_clone_prompt": voice_clone_prompt,
    },
)
resp.raise_for_status()

# Save streamed WAV audio
with open("output.wav", "wb") as f:
    f.write(resp.content)
```

## Explore Examples

```bash
# See basic usage
python examples/01_basic_usage.py

# See API client usage
python examples/02_api_client.py

# See complete workflow
python examples/03_full_workflow.py

# See batch processing
python examples/04_batch_processing.py
```

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run fast tests only
pytest tests/ -m "not slow and not requires_gpu"

# Coverage report
pytest tests/ --cov=src/voice_cloning
```

## Audio Requirements

For best results, prepare audio with:

- **Format**: WAV file
- **Duration**: 5-30 seconds
- **Quality**: Clear speech, minimal background noise
- **Sample Rate**: 16kHz or 24kHz recommended
- **Transcript**: Exact text spoken in the audio

## API Endpoints

```
POST   /api/v1/create-prompt  - Create voice clone from audio (returns serialized prompt object)
POST   /api/v1/synthesize     - Generate audio with cloned voice (streams WAV audio)
GET    /api/v1/download/{id}  - Download audio file (legacy file-based flow)
GET    /api/v1/prompts        - List cached voice prompts
DELETE /api/v1/prompts/{id}   - Delete voice prompt
GET    /api/v1/health         - Check server status
```

## Common Tasks

### Task: List cached voices

```python
prompts = engine.list_cached_prompts()
print(prompts)
```

### Task: Switch to different voice

```python
# Synthesize with a different speaker's voice
audio = engine.synthesize_voice(
    text='Same text, different voice',
    prompt_name='different_voice'  # Just change the prompt name
)
```

### Task: Clear memory cache

```python
engine.clear_prompt_cache()
```

### Task: Use different language

```python
audio = engine.synthesize_voice(
    text='你好，这是合成语音。',  # Chinese text
    language='Chinese',
    prompt_name='my_voice'
)
```

## Supported Languages

- Auto (automatic detection)
- English
- Chinese
- Japanese
- Korean
- German
- French
- Russian
- Portuguese
- Spanish
- Italian

## Troubleshooting

**Q: It's slow on my machine**

- Use GPU if available (auto-detected)
- Use `torch.float32` dtype if GPU runs out of memory

**Q: Out of memory errors**

- Clear prompt cache: `engine.clear_prompt_cache()`
- Use lower batch size in config
- Use CPU preset config

**Q: Poor audio quality**

- Use clearer source audio (less background noise)
- Longer audio clips (10-20 seconds) work better
- Ensure transcript matches audio exactly

**Q: Module not found error**

- Install package: `pip install -e .`
- Add to PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"`

## Next Steps

1. **Try the examples**: `python examples/01_basic_usage.py`
2. **Run the tests**: `pytest tests/ -v`
3. **Read the docs**: See `examples/README.md` and `tests/README.md`
4. **Start your own**: Copy example and modify for your use case

## Resources

- **Examples**: `examples/` directory (4 complete workflows)
- **Tests**: `tests/` directory (200+ test cases)
- **Documentation**: See individual `README.md` files
- **API Docs**: `api/API.md` for REST endpoint details
- **Structure**: `PROJECT_STRUCTURE.md` for architecture overview

## Hardware Detection

The system automatically detects your hardware:

```python
# Auto-detection
from voice_cloning.config import get_recommended_config_for_hardware
config = get_recommended_config_for_hardware()
print(config.get_device_info())  # Shows detected device

# Or specify manually
from voice_cloning.config import get_config
config = get_config('cpu')        # Force CPU
config = get_config('standard_gpu')  # Use GPU
```

## Support

For issues or questions:

1. Check the `examples/` directory for patterns
2. Run matching test: `pytest tests/test_config.py -v`
3. Review documentation in `README.md` files
4. Check troubleshooting sections in example files

---

**Ready to start?** Run: `python examples/01_basic_usage.py`
