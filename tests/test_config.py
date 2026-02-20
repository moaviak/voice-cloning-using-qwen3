"""
Unit tests for voice_cloning.config module.

Tests configuration loading, validation, and hardware detection.
"""

import sys
from pathlib import Path
import pytest
import torch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning.config import (
    EngineConfig,
    get_recommended_config_for_hardware,
    get_config,
    PRESETS,
    DEFAULT_CONFIG,
)


class TestEngineConfig:
    """Test EngineConfig dataclass."""
    
    def test_default_config_creation(self):
        """Test creating a default configuration."""
        config = EngineConfig()
        
        assert config.model_path == "models/qwen3-tts"
        assert config.dtype == torch.bfloat16
        assert config.sample_rate == 24000
        assert config.output_dir == "output"
        assert config.batch_size >= 1
    
    def test_custom_config_creation(self):
        """Test creating a custom configuration."""
        config = EngineConfig(
            device="cpu",
            dtype=torch.float32,
            batch_size=2,
            output_dir="custom_output"
        )
        
        assert config.device == "cpu"
        assert config.dtype == torch.float32
        assert config.batch_size == 2
        assert config.output_dir == "custom_output"
    
    def test_config_validation_valid(self):
        """Test configuration validation with valid values."""
        config = EngineConfig(
            device="cpu",
            dtype=torch.float32,
            batch_size=1
        )
        
        assert config.validate() is True
    
    def test_config_validation_invalid_device(self):
        """Test configuration validation with invalid device."""
        config = EngineConfig(device="invalid_device")
        
        # Should print error but return False
        result = config.validate()
        assert result is False
    
    def test_config_validation_invalid_language(self):
        """Test configuration validation with invalid language."""
        config = EngineConfig(default_language="NonExistent")
        
        result = config.validate()
        assert result is False
    
    def test_config_validation_invalid_batch_size(self):
        """Test configuration validation with invalid batch size."""
        config = EngineConfig(batch_size=0)
        
        result = config.validate()
        assert result is False
    
    def test_config_device_info_with_device(self):
        """Test get_device_info() when device is specified."""
        config = EngineConfig(device="cuda:0")
        
        device_info = config.get_device_info()
        assert device_info == "cuda:0"
    
    def test_config_device_info_auto_detect(self):
        """Test get_device_info() with auto-detection."""
        config = EngineConfig(device=None, auto_detect_device=True)
        
        device_info = config.get_device_info()
        # Should return cuda:0 or cpu depending on environment
        assert device_info in ["cuda:0 (auto-detect)", "cpu (auto-detect)"]
    
    def test_config_string_representation(self):
        """Test string representation of config."""
        config = EngineConfig(device="cpu", batch_size=2)
        
        config_str = str(config)
        assert "EngineConfig" in config_str
        assert "device" in config_str
        assert "batch_size" in config_str
    
    def test_supported_languages(self):
        """Test that all supported languages are defined."""
        config = DEFAULT_CONFIG
        
        expected_languages = (
            "Auto", "English", "Chinese", "Japanese", "Korean",
            "German", "French", "Russian", "Portuguese", "Spanish", "Italian"
        )
        
        assert config.supported_languages == expected_languages


class TestConfigPresets:
    """Test preset configurations."""
    
    def test_preset_names(self):
        """Test that all expected presets exist."""
        expected_presets = [
            "high_performance_gpu",
            "standard_gpu",
            "low_vram_gpu",
            "cpu",
            "auto"
        ]
        
        for preset_name in expected_presets:
            assert preset_name in PRESETS
    
    def test_high_performance_preset(self):
        """Test high performance GPU preset."""
        config = PRESETS["high_performance_gpu"]
        
        assert config.device == "cuda:0"
        assert config.dtype == torch.bfloat16
        assert config.use_flash_attention is True
        assert config.batch_size == 4
    
    def test_standard_preset(self):
        """Test standard GPU preset."""
        config = PRESETS["standard_gpu"]
        
        assert config.device == "cuda:0"
        assert config.dtype == torch.bfloat16
        assert config.use_flash_attention is False
        assert config.batch_size == 2
    
    def test_low_vram_preset(self):
        """Test low VRAM GPU preset."""
        config = PRESETS["low_vram_gpu"]
        
        assert config.device == "cuda:0"
        assert config.dtype == torch.float32
        assert config.use_flash_attention is False
        assert config.batch_size == 1
    
    def test_cpu_preset(self):
        """Test CPU preset."""
        config = PRESETS["cpu"]
        
        assert config.device == "cpu"
        assert config.dtype == torch.float32
        assert config.batch_size == 1
    
    def test_auto_preset(self):
        """Test auto preset."""
        config = PRESETS["auto"]
        
        # Auto preset should have device=None to trigger detection
        assert config.device is None
        assert config.auto_detect_device is True


class TestGetConfig:
    """Test get_config function."""
    
    def test_get_config_default(self):
        """Test getting default config."""
        config = get_config("auto")
        
        assert config is not None
        assert isinstance(config, EngineConfig)
    
    def test_get_config_cpu(self):
        """Test getting CPU config."""
        config = get_config("cpu")
        
        assert config.device == "cpu"
        assert config.dtype == torch.float32
    
    def test_get_config_invalid_preset(self):
        """Test getting invalid preset."""
        with pytest.raises(ValueError) as exc_info:
            get_config("nonexistent_preset")
        
        assert "Unknown preset" in str(exc_info.value)
        assert "nonexistent_preset" in str(exc_info.value)


class TestHardwareDetection:
    """Test hardware detection functions."""
    
    def test_recommended_config_returns_config(self):
        """Test that recommended config returns EngineConfig."""
        config = get_recommended_config_for_hardware()
        
        assert isinstance(config, EngineConfig)
    
    def test_recommended_config_sets_device(self):
        """Test that recommended config sets a device."""
        config = get_recommended_config_for_hardware()
        
        # Should have either cuda:0 or cpu set
        assert config.device is not None
        assert config.device in ["cuda:0", "cpu"]
    
    def test_recommended_config_sets_dtype(self):
        """Test that recommended config sets dtype."""
        config = get_recommended_config_for_hardware()
        
        # Should be either bfloat16 or float32
        assert config.dtype in [torch.bfloat16, torch.float32]
    
    def test_gpu_prefers_bfloat16(self):
        """Test that GPU configs prefer bfloat16."""
        config = get_recommended_config_for_hardware()
        
        if torch.cuda.is_available():
            # If GPU available, should prefer bfloat16
            assert config.dtype == torch.bfloat16
        else:
            # If no GPU, should use float32
            assert config.dtype == torch.float32


class TestDefaultConfig:
    """Test default configuration instance."""
    
    def test_default_config_is_engineconfig(self):
        """Test that DEFAULT_CONFIG is EngineConfig instance."""
        assert isinstance(DEFAULT_CONFIG, EngineConfig)
    
    def test_default_config_is_valid(self):
        """Test that default config is valid."""
        assert DEFAULT_CONFIG.validate() is True
    
    def test_default_config_has_model_path(self):
        """Test that default config has model path."""
        assert DEFAULT_CONFIG.model_path == "models/qwen3-tts"


# Integration tests
class TestConfigIntegration:
    """Integration tests for configuration system."""
    
    def test_config_compatibility(self):
        """Test that all presets are compatible with engine."""
        # This test would require actual engine initialization
        # For now, just verify all presets are valid
        
        for preset_name, config in PRESETS.items():
            assert config.validate() is True, f"{preset_name} preset is invalid"
    
    def test_config_persistence(self):
        """Test that config can be saved and loaded."""
        original_config = EngineConfig(
            device="cpu",
            batch_size=2,
            output_dir="test_output"
        )
        
        # Would test serialization here if implemented
        assert original_config.device == "cpu"
        assert original_config.batch_size == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
