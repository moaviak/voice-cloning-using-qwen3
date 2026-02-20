"""
Pytest configuration and fixtures for voice cloning tests.

Provides:
- Temporary directories for test outputs
- Mock models and audio files
- Reusable fixtures for all tests
"""

import pytest
import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def test_output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_audio_file(test_data_dir):
    """Create a sample audio file for testing."""
    import soundfile as sf
    
    # Create simple audio: 24kHz, 5 seconds (simple sine wave)
    sample_rate = 24000
    duration = 5  # seconds
    
    # Generate simple audio
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Simple sine wave at 440 Hz
    audio = 0.3 * np.sin(2 * np.pi * 440 * t)
    
    # Save audio file
    audio_path = test_data_dir / "sample_audio.wav"
    sf.write(str(audio_path), audio, sample_rate)
    
    return audio_path


@pytest.fixture
def config_with_test_settings():
    """Create a test configuration."""
    from voice_cloning.config import EngineConfig
    import torch
    
    return EngineConfig(
        model_path="models/qwen3-tts",
        device="cpu",  # Use CPU for testing
        dtype=torch.float32,
        auto_detect_device=False,
        verbose=False,
    )


@pytest.fixture
def engine(config_with_test_settings):
    """Create a test engine instance.
    
    NOTE: This requires the actual model files to be present.
    For unit tests without models, use mocks instead.
    """
    try:
        from voice_cloning import VoiceCloningEngine
        return VoiceCloningEngine(config_with_test_settings)
    except Exception as e:
        pytest.skip(f"Could not initialize engine: {e}")


# Test data constants
SAMPLE_TRANSCRIPT = "Hello, this is a test transcript for voice cloning."
SAMPLE_SYNTHESIS_TEXT = "This is synthesized speech from the cloned voice."
SAMPLE_PROMPT_NAME = "test_voice"


@pytest.fixture(scope="session")
def test_constants():
    """Provide test constants."""
    return {
        "transcript": SAMPLE_TRANSCRIPT,
        "synthesis_text": SAMPLE_SYNTHESIS_TEXT,
        "prompt_name": SAMPLE_PROMPT_NAME,
    }


def pytest_configure(config):
    """Pytest configuration hook."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "requires_model: marks tests that require model files"
    )
    config.addinivalue_line(
        "markers", "requires_gpu: marks tests that require GPU"
    )


# Markers for common use cases
pytestmark = [
    pytest.mark.requires_model,  # Most tests require model files
]
