# Migration Guide: New Project Structure

This guide explains the changes in the new modularized project structure and how to update your code.

## What Changed?

The project has been reorganized from a flat structure to a modular package structure for better maintainability and scalability.

### Old Structure

```
voice-cloning-using-qwen3/
├── qwen3_voice_engine.py         # Core engine
├── config.py                      # Configuration
├── api/
│   ├── api.py                     # API application
│   ├── run_api.py                 # API runner
│   └── ...
├── examples.py                    # Examples
├── applications.py
└── ...
```

### New Structure

```
voice-cloning-using-qwen3/
├── src/
│   └── voice_cloning/             # Main package
│       ├── core/                  # Engine module
│       ├── config/                # Configuration module
│       ├── api/                   # API module
│       └── utils/                 # Utilities
├── examples/                      # Example scripts
├── scripts/                       # CLI scripts
├── tests/                         # Tests
├── docs/                          # Documentation
└── setup.py                       # Package setup
```

## Import Changes

### Old Imports

```python
from qwen3_voice_engine import VoiceCloningEngine
from config import get_recommended_config_for_hardware, EngineConfig
```

### New Imports

```python
from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware, EngineConfig
```

## How to Update Your Code

### If You Were Using the Engine Directly

**Before:**

```python
import sys
sys.path.insert(0, '.')

from qwen3_voice_engine import VoiceCloningEngine
from config import get_recommended_config_for_hardware

config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(...)
```

**After:**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(...)
```

Or (if installed as package):

```python
from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware

config = get_recommended_config_for_hardware()
engine = VoiceCloningEngine(...)
```

### If You Were Using the API

**Before:**

```python
python api/run_api.py
```

**After:**

```python
python scripts/run_api.py
```

Or:

```bash
python -m uvicorn voice_cloning.api:app --reload
```

### If You Were Running Tests

**Before:**

```bash
python test_setup.py
```

**After:**

```bash
pytest  # For all tests
pytest tests/test_api.py  # Specific test file
```

## Installation Options

### Option 1: Development Installation (Recommended)

Install the package in development mode:

```bash
pip install -e .
```

This allows you to:

- Import from `voice_cloning` anywhere
- Edit code and see changes immediately
- Proper package management with `pip`

### Option 2: Temporary Path Modification

For scripts, add to beginning:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_cloning.core import VoiceCloningEngine
from voice_cloning.config import get_recommended_config_for_hardware
```

### Option 3: PYTHONPATH Environment Variable

Set before running:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python your_script.py
```

## File Locations Reference

| Component            | Old Location                  | New Location                                 |
| -------------------- | ----------------------------- | -------------------------------------------- |
| Core Engine          | `qwen3_voice_engine.py`       | `src/voice_cloning/core/__init__.py`         |
| Configuration        | `config.py`                   | `src/voice_cloning/config/__init__.py`       |
| FastAPI App          | `api/api.py` (monolithic)     | `src/voice_cloning/api/main.py` (modular)    |
| Health Endpoints     | `api/api.py`                  | `src/voice_cloning/api/routes/health.py`     |
| Synthesis Endpoints  | `api/api.py`                  | `src/voice_cloning/api/routes/synthesis.py`  |
| Management Endpoints | `api/api.py`                  | `src/voice_cloning/api/routes/management.py` |
| API Models           | `api/api.py`                  | `src/voice_cloning/api/models/__init__.py`   |
| API Utilities        | `api/api.py`                  | `src/voice_cloning/api/utils/__init__.py`    |
| API Runner           | `api/run_api.py`              | `scripts/run_api.py`                         |
| Basic Examples       | `examples.py`                 | `examples/basic_examples.py`                 |
| Applications         | `applications.py`             | `examples/applications.py`                   |
| Quickstart           | `quickstart.py`               | `examples/quickstart.py`                     |
| Setup/Config         | `config.py`, individual files | `setup.py`, `requirements.txt`               |

## CLI Commands Updates

### Old Commands

```bash
# Run API
python api/run_api.py

# Run examples
python examples.py
python applications.py
python quickstart.py

# Run tests
python test_setup.py
```

### New Commands

```bash
# Run API
python scripts/run_api.py

# Run examples
python examples/basic_examples.py
python examples/api_examples.py
python examples/applications.py
python examples/quickstart.py

# Run tests
pytest  # All tests
pytest tests/test_engine.py  # Specific test
pytest --cov=src/voice_cloning  # With coverage

# If installed as package
voice-api  # Run API (future)
```

## Backward Compatibility

The old top-level files remain in the root directory for backward compatibility:

- `qwen3_voice_engine.py` - Original engine (imports from new location)
- `config.py` - Original config (imports from new location)

These files will be removed in a future version. Update your code to use new imports.

## Benefits of New Structure

✅ **Better Organization** - Clear module boundaries
✅ **Package Management** - Install with `pip install -e .`
✅ **Scalability** - Easy to add new modules
✅ **Testing** - Proper test organization
✅ **Documentation** - Clear API structure
✅ **Development** - Easier to contribute and maintain
✅ **Deployment** - Professional package deployment

## Common Issues and Solutions

### Issue 1: ImportError: No module named 'voice_cloning'

**Solution 1** - Install package:

```bash
pip install -e .
```

**Solution 2** - Add path to sys.path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

**Solution 3** - Use PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python your_script.py
```

### Issue 2: Can't find model files

Make sure `models/qwen3-tts/` is in the project root:

```bash
voice-cloning-using-qwen3/
├── models/
│   └── qwen3-tts/
│       ├── model.safetensors
│       ├── config.json
│       └── ...
├── src/
│   └── voice_cloning/
...
```

### Issue 3: Can't import from api.py directly

The old `api.py` monolithic file is now split into modules. Import from:

```python
from voice_cloning.api import app, create_app
from voice_cloning.api.models import PromptResponse
from voice_cloning.api.routes import health, synthesis, management
```

## Getting Help

If you encounter issues:

1. Check PROJECT_STRUCTURE.md for detailed structure
2. Look at examples/ for usage patterns
3. Run tests to verify installation
4. Check docs/ for detailed documentation

## Next Steps

1. **Install the Package**:

   ```bash
   pip install -e .
   ```

2. **Update Your Scripts**:
   - Change imports from `qwen3_voice_engine` to `voice_cloning.core`
   - Change imports from `config` to `voice_cloning.config`

3. **Verify Installation**:

   ```bash
   # Run basic example
   python examples/basic_examples.py

   # Run tests
   pytest
   ```

4. **Run API** (if using):
   ```bash
   python scripts/run_api.py
   ```

## Questions?

Refer to:

- `PROJECT_STRUCTURE.md` - Detailed structure explanation
- `docs/` - Complete documentation
- `examples/` - Usage examples
- `tests/` - Test examples
