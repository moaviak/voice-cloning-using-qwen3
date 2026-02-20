# Voice Cloning Examples

This directory contains comprehensive examples demonstrating how to use the Voice Cloning Engine and REST API.

## Quick Navigation

| Example                                     | Purpose           | Use Case               |
| ------------------------------------------- | ----------------- | ---------------------- |
| [01_basic_usage.py](#basic-usage)           | Direct engine API | Development & testing  |
| [02_api_client.py](#api-client)             | REST API client   | Web apps, remote usage |
| [03_full_workflow.py](#full-workflow)       | Complete pipeline | Production workflows   |
| [04_batch_processing.py](#batch-processing) | Batch operations  | Large-scale processing |

---

## Basic Usage

**File**: `01_basic_usage.py`

The simplest way to use voice cloning - directly interact with the engine.

### What it demonstrates:

- Initialize the engine with auto hardware detection
- Create a voice clone from audio + transcript
- Synthesize audio using the stored prompt
- Manage cached voice prompts

### Quick Example:

```python
from voice_cloning import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

# Initialize
config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(config)

# Create voice clone
prompt_id = engine.create_voice_clone_prompt(
    audio_path='voice_samples/john.wav',
    transcript='Hello, this is John speaking.',
    prompt_name='john_voice'
)

# Synthesize audio
audio = engine.synthesize_voice(
    text='The new text to synthesize',
    language='English',
    prompt_name='john_voice'
)

# Save output
import soundfile as sf
sf.write('output_john.wav', audio, 24000)
```

### Run it:

```bash
python examples/01_basic_usage.py
```

---

## API Client

**File**: `02_api_client.py`

Use voice cloning via HTTP REST API endpoints.

### What it demonstrates:

- Initialize API client
- Create voice clones via POST endpoint
- Synthesize audio via POST endpoint
- List and manage cached prompts
- Download synthesized audio files

### Quick Example:

```python
from examples.api_client import VoiceCloningAPIClient

# Initialize client (server must be running)
client = VoiceCloningAPIClient(base_url="http://localhost:8000")

# Check server health
status = client.check_health()
print(f"Server device: {status['device']}")

# Create voice clone
response = client.create_voice_clone(
    audio_file='voice_samples/john.wav',
    transcript='Hello, this is John speaking.',
    prompt_name='john_voice'
)

# Synthesize audio
audio_data = client.synthesize_audio(
    text='New text to synthesize',
    prompt_name='john_voice',
    language='English'
)

# Save audio
with open('output.wav', 'wb') as f:
    f.write(audio_data)
```

### Start the API server:

```bash
python scripts/run_api.py --port 8000 --reload
```

### Run the client example:

```bash
python examples/02_api_client.py
```

### Available endpoints:

- `POST   /api/v1/create-prompt` - Create voice clone
- `POST   /api/v1/synthesize` - Synthesize audio
- `GET    /api/v1/download/{filename}` - Download file
- `GET    /api/v1/prompts` - List prompts
- `DELETE /api/v1/prompts/{id}` - Delete prompt
- `GET    /api/v1/health` - Server status

---

## Full Workflow

**File**: `03_full_workflow.py`

Comprehensive guide to production-quality voice cloning workflows.

### What it demonstrates:

- Engine initialization and configuration
- Voice clone creation from audio
- Managing voice prompts
- Batch text synthesis
- Memory management
- Error handling patterns
- Language support

### Key sections:

1. **Step 1**: Initialize engine with optimal configuration
2. **Step 2**: Create voice clones from reference audio
3. **Step 3**: Manage and list cached prompts
4. **Step 4**: Batch synthesis with multiple texts
5. **Step 5**: Memory management strategies
6. **Step 6**: Production-quality error handling

### Run it:

```bash
python examples/03_full_workflow.py
```

### Supported Languages:

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

---

## Batch Processing

**File**: `04_batch_processing.py`

Advanced patterns for processing multiple files and large-scale synthesis.

### What it demonstrates:

- Create multiple voice clones in batch
- Synthesize multiple texts with one voice
- Production pipeline patterns
- Progress tracking and logging
- Error handling with continuation
- Memory-efficient processing

### Key classes:

- `BatchVoiceCloningProcessor`: Helper for batch operations

### Example scenarios:

1. **Multiple Speaker Cloning**: Create voices for 3+ speakers
2. **Large-Scale Synthesis**: Generate 100+ audio files
3. **Production Pipeline**: Handle directory of audio files

### Production Pipeline Pattern:

```python
class ProductionPipeline:
    def __init__(self, config):
        self.engine = VoiceCloningEngine(config)
        self.processor = BatchVoiceCloningProcessor(self.engine)

    def process_directory(self, audio_dir, output_dir):
        # Find all audio files
        audio_files = {}
        for wav_file in Path(audio_dir).glob('*.wav'):
            txt_file = wav_file.with_suffix('.txt')
            if txt_file.exists():
                transcript = txt_file.read_text().strip()
                audio_files[wav_file.stem] = (str(wav_file), transcript)

        # Create prompts
        results = self.processor.batch_create_prompts(audio_files)

        # Log results
        return results
```

### Run it:

```bash
python examples/04_batch_processing.py
```

---

## Common Tasks

### Task: Create a voice clone

```python
prompt_id = engine.create_voice_clone_prompt(
    audio_path='path/to/audio.wav',
    transcript='Exact text spoken in the audio',
    prompt_name='unique_name'
)
```

### Task: Synthesize text with cloned voice

```python
audio = engine.synthesize_voice(
    text='Text to synthesize',
    language='English',  # or 'Auto' for auto-detection
    prompt_name='unique_name'
)

# Save to file
import soundfile as sf
sf.write('output.wav', audio, 24000)
```

### Task: List cached voice prompts

```python
prompts = engine.list_cached_prompts()
print(prompts)
```

### Task: Clear cached prompts

```python
engine.clear_prompt_cache()
```

### Task: Use the API instead of direct engine

```python
# All the same operations work via REST API
# Just use VoiceCloningAPIClient instead of VoiceCloningEngine
```

---

## Best Practices

### Audio Quality

- **Duration**: 5-30 seconds of clear speech recommended
- **Sample Rate**: 16kHz or 24kHz
- **Quality**: Minimal background noise
- **Format**: WAV (mono or stereo, mono preferred)

### Transcript Accuracy

- Match the audio content precisely
- Include proper punctuation
- Use correct capitalization
- Proofread before using

### Memory Management

- Monitor cached prompts count
- Clear cache when not needed
- Use `list_cached_prompts()` to check
- Clear with `clear_prompt_cache()`

### Error Handling

```python
try:
    prompt_id = engine.create_voice_clone_prompt(...)
except FileNotFoundError:
    print("Audio file not found")
except ValueError:
    print("Invalid settings")
except RuntimeError:
    print("Processing error")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Performance Tips

1. Use GPU when available (auto-detected)
2. Batch operations for efficiency
3. Use appropriate dtype (bfloat16 for GPU, float32 for CPU)
4. Process multiple texts in sequence
5. Manage memory by clearing cache regularly

---

## Troubleshooting

### Common Issues

**Q: ModuleNotFoundError: No module named 'voice_cloning'**

- Make sure you're running from the project root
- Or install package: `pip install -e .`

**Q: API server connection refused**

- Start the server first: `python scripts/run_api.py`
- Check that port 8000 is available

**Q: Out of memory errors**

- Use lower dtype: `torch.float32` instead of `bfloat16`
- Clear cache: `engine.clear_prompt_cache()`
- Reduce batch size in config

**Q: Poor audio quality**

- Ensure transcript matches audio exactly
- Use cleaner audio (less background noise)
- Try longer duration audio (10-20 seconds)

### Getting Help

1. Check PROJECT_STRUCTURE.md for architecture overview
2. Check MIGRATION.md for import paths
3. Review API.md for endpoint documentation
4. Look at actual code in src/voice_cloning/

---

## Environment Setup

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Optional: Install in development mode:

```bash
pip install -e .
```

### Check installation:

```bash
python -c "from voice_cloning import VoiceCloningEngine; print('✓ Installation OK')"
```

---

## Next Steps

1. **Start with**: 01_basic_usage.py (direct engine)
2. **Then try**: 03_full_workflow.py (complete example)
3. **For production**: 04_batch_processing.py (batch operations)
4. **For web apps**: 02_api_client.py (REST API)

---

## Related Documentation

- [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - Architecture overview
- [MIGRATION.md](../MIGRATION.md) - For updating existing code
- [API.md](../api/API.md) - REST API documentation
- [README.md](../README.md) - Project overview

---

## Questions?

Check the comments in each example file for detailed explanations and additional code samples.
