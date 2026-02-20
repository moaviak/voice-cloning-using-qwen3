# Voice Cloning Tests

This directory contains comprehensive tests for the voice cloning system, covering configuration, API models, core engine functionality, and integration scenarios.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_config.py           # Configuration module tests
├── test_api_models.py       # API request/response model tests
├── test_engine.py           # Core engine functionality tests
└── README.md               # This file
```

## Test Categories

### 1. Configuration Tests (`test_config.py`)

Tests the engine configuration system:

- EngineConfig dataclass creation and validation
- Configuration presets (CPU, GPU high/low performance)
- Hardware detection
- Language support validation

**Run**: `pytest tests/test_config.py -v`

### 2. API Models Tests (`test_api_models.py`)

Tests request/response Pydantic models:

- PromptResponse model
- SynthesisRequest model
- SynthesisResponse model
- EngineStatus model
- JSON serialization

**Run**: `pytest tests/test_api_models.py -v`

### 3. Engine Tests (`test_engine.py`)

Tests core voice cloning engine:

- Engine initialization
- Voice prompt management
- Voice synthesis
- Hardware detection
- Method signatures

**Requirements**: Requires model files in `models/qwen3-tts/`

**Run**: `pytest tests/test_engine.py -v -m requires_model`

### 4. Conftest Fixtures (`conftest.py`)

Provides reusable test fixtures:

- `project_root`: Project root directory
- `test_data_dir`: Temporary test data directory
- `test_output_dir`: Temporary output directory
- `sample_audio_file`: Generated test audio file
- `config_with_test_settings`: Pre-configured test engine config
- `engine`: Initialized engine instance

## Running Tests

### Basic Usage

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run specific test class
pytest tests/test_config.py::TestEngineConfig -v

# Run specific test
pytest tests/test_config.py::TestEngineConfig::test_default_config_creation -v
```

### Using Markers

```bash
# Skip slow tests
pytest tests/ -v -m "not slow"

# Skip GPU tests
pytest tests/ -v -m "not requires_gpu"

# Only tests requiring models
pytest tests/ -v -m requires_model

# Skip everything requiring models
pytest tests/ -v -m "not requires_model"
```

### Coverage Analysis

```bash
# Generate coverage report
pytest tests/ --cov=src/voice_cloning --cov-report=html

# View HTML report
open htmlcov/index.html
```

### Continuous Integration

```bash
# Fast tests (skip slow and GPU tests)
pytest tests/ -v -m "not slow and not requires_gpu and not requires_model"

# Full test suite
pytest tests/ -v --cov=src/voice_cloning
```

## Test Markers

Test markers help you run specific test subsets:

### Available Markers

- **@pytest.mark.slow**: Tests that take > 1 minute
  - Skip with: `pytest -m "not slow"`
- **@pytest.mark.requires_gpu**: Tests requiring GPU
  - Skip with: `pytest -m "not requires_gpu"`
- **@pytest.mark.requires_model**: Tests requiring model files
  - Skip with: `pytest -m "not requires_model"`

### Example Marker Usage

```python
@pytest.mark.slow
def test_large_batch_synthesis():
    """This test takes a long time."""
    pass

@pytest.mark.requires_gpu
def test_gpu_acceleration():
    """This test requires CUDA GPU."""
    pass

@pytest.mark.requires_model
def test_engine_initialization():
    """This test requires model files."""
    pass
```

## Test Fixtures

### Using Built-in Fixtures

```python
def test_something(project_root, test_output_dir, sample_audio_file):
    """Test using provided fixtures."""
    assert project_root.exists()
    assert test_output_dir.exists()
    assert sample_audio_file.exists()
```

### Custom Fixtures

Create fixtures in `conftest.py`:

```python
@pytest.fixture
def custom_config():
    """Create a custom configuration."""
    return EngineConfig(device="cpu", batch_size=2)
```

## Common Test Patterns

### Testing Configuration

```python
def test_config_validation():
    config = EngineConfig(device="cpu")
    assert config.validate() is True
```

### Testing with Temporary Files

```python
def test_file_processing(test_data_dir, test_output_dir):
    input_file = test_data_dir / "input.wav"
    output_file = test_output_dir / "output.wav"

    # Process file
    # Assert output exists
    assert output_file.exists()
```

### Testing Engine Methods

```python
@pytest.mark.requires_model
def test_engine_synthesis(engine, test_constants):
    audio = engine.synthesize_voice(
        text=test_constants["synthesis_text"],
        language="English",
        prompt_name=test_constants["prompt_name"]
    )
    assert audio is not None
    assert len(audio) > 0
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest tests/ -v -m "not slow and not requires_gpu and not requires_model"

      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### Test Failures

**Q: Tests fail with "ModuleNotFoundError"**

- Make sure src/ is in Python path
- Install package: `pip install -e .`

**Q: Tests require model but files aren't present**

- Download models: `python download_models.py`
- Or skip model tests: `pytest -m "not requires_model"`

**Q: GPU tests fail but GPU is available**

- Check CUDA availability: `python -c "import torch; print(torch.cuda.is_available())"`
- Verify model file location
- Check VRAM availability

**Q: Slow tests timeout**

- Increase timeout: `pytest tests/ --timeout=600`
- Or skip slow tests: `pytest -m "not slow"`

### Debugging Tests

```bash
# Run with verbose output
pytest tests/test_config.py -vv

# Show print statements
pytest tests/test_config.py -v -s

# Stop on first error
pytest tests/test_config.py -x

# Run last failed tests
pytest tests/ --lf

# Run failed tests first
pytest tests/ --ff

# Drop into debugger on error
pytest tests/ --pdb
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test names should describe what they test
3. **Fixtures**: Use fixtures for common setup/teardown
4. **Markers**: Use markers for test categorization
5. **Mocking**: Mock external dependencies (models, APIs)
6. **Coverage**: Aim for > 80% code coverage
7. **Speed**: Keep tests fast, use markers for slow tests

## Adding New Tests

1. Create test function prefixed with `test_`
2. Use descriptive names: `test_<function>_<scenario>`
3. Add docstrings explaining what's tested
4. Use appropriate fixtures
5. Add markers if needed
6. Run manually first: `pytest tests/test_new.py -v`

Example:

```python
def test_config_cpu_device(config_with_test_settings):
    """Test that config properly sets CPU device."""
    assert config_with_test_settings.device == "cpu"
    assert config_with_test_settings.dtype == torch.float32
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Fixtures Documentation](https://docs.pytest.org/en/6.2.x/fixture.html)
- [Markers Documentation](https://docs.pytest.org/en/6.2.x/mark.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

## Questions?

Check individual test files for examples specific to each module.
