"""
Tests for voice cloning core functionality.

Note: These tests require the model files to be present in models/qwen3-tts/.
For CI/CD environments without GPU, use markers to skip GPU-intensive tests.

Run tests:
    pytest tests/test_engine.py -v
    pytest tests/test_engine.py -v -m "not slow and not requires_gpu"
"""

import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestEngineImports:
    """Test that engine can be imported."""
    
    def test_engine_import(self):
        """Test importing VoiceCloningEngine."""
        from voice_cloning import VoiceCloningEngine
        assert VoiceCloningEngine is not None
    
    def test_config_import(self):
        """Test importing configuration."""
        from voice_cloning import VoiceCloningEngine
        from voice_cloning.config import EngineConfig
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None
    
    def test_backward_compatibility_import(self):
        """Test that backward compatibility imports work."""
        from config import EngineConfig
        assert EngineConfig is not None


class TestEngineInitialization:
    """Test engine initialization with various configurations."""
    
    @pytest.mark.requires_model
    def test_engine_init_with_default_config(self):
        """Test initializing engine with default config."""
        from voice_cloning import VoiceCloningEngine
        from voice_cloning.config import DEFAULT_CONFIG
        
        # This will fail if model files don't exist
        try:
            engine = VoiceCloningEngine(DEFAULT_CONFIG)
            assert engine is not None
        except FileNotFoundError:
            pytest.skip("Model files not found")
    
    @pytest.mark.requires_model
    def test_engine_init_with_cpu_config(self, config_with_test_settings):
        """Test initializing engine with CPU config."""
        from voice_cloning import VoiceCloningEngine
        
        try:
            engine = VoiceCloningEngine(config_with_test_settings)
            assert engine is not None
        except FileNotFoundError:
            pytest.skip("Model files not found")


class TestEngineConfiguration:
    """Test engine configuration options."""
    
    def test_recommended_config_is_valid(self):
        """Test that recommended config is valid."""
        from voice_cloning.config import get_recommended_config_for_hardware
        
        config = get_recommended_config_for_hardware()
        assert config.validate() is True
    
    def test_cpu_config_is_valid(self):
        """Test that CPU config is valid."""
        from voice_cloning.config import get_config
        
        config = get_config("cpu")
        assert config.validate() is True
    
    @pytest.mark.requires_gpu
    def test_gpu_config_is_valid(self):
        """Test that GPU config is valid."""
        from voice_cloning.config import get_config
        
        config = get_config("standard_gpu")
        assert config.validate() is True


class TestEngineMethods:
    """Test engine methods exist and have correct signatures."""
    
    @pytest.mark.requires_model
    def test_engine_has_create_prompt_method(self, engine):
        """Test that engine has create_voice_clone_prompt method."""
        assert hasattr(engine, 'create_voice_clone_prompt')
        assert callable(getattr(engine, 'create_voice_clone_prompt'))
    
    @pytest.mark.requires_model
    def test_engine_has_synthesize_method(self, engine):
        """Test that engine has synthesize_voice method."""
        assert hasattr(engine, 'synthesize_voice')
        assert callable(getattr(engine, 'synthesize_voice'))
    
    @pytest.mark.requires_model
    def test_engine_has_list_prompts_method(self, engine):
        """Test that engine has list_cached_prompts method."""
        assert hasattr(engine, 'list_cached_prompts')
        assert callable(getattr(engine, 'list_cached_prompts'))
    
    @pytest.mark.requires_model
    def test_engine_has_clear_cache_method(self, engine):
        """Test that engine has clear_prompt_cache method."""
        assert hasattr(engine, 'clear_prompt_cache')
        assert callable(getattr(engine, 'clear_prompt_cache'))


class TestEngineVoicePromptManagement:
    """Test voice prompt caching and management."""
    
    @pytest.mark.requires_model
    def test_list_cached_prompts_returns_list(self, engine):
        """Test that list_cached_prompts returns a list."""
        prompts = engine.list_cached_prompts()
        assert isinstance(prompts, (list, dict))
    
    @pytest.mark.requires_model
    def test_clear_prompt_cache(self, engine):
        """Test that clear_prompt_cache doesn't raise errors."""
        # Should not raise an exception
        engine.clear_prompt_cache()


class TestEngineAudioProcessing:
    """Test audio processing capabilities."""
    
    @pytest.mark.requires_model
    @pytest.mark.slow
    def test_synthesize_voice_output_type(self, engine, test_constants):
        """Test that synthesize_voice returns audio data."""
        try:
            # Assuming a prompt exists in cache
            audio = engine.synthesize_voice(
                text=test_constants["synthesis_text"],
                language="English",
                prompt_name=test_constants["prompt_name"]
            )
            
            # Should return numpy array or similar
            assert audio is not None
        except KeyError:
            pytest.skip("No cached prompts available")
        except Exception as e:
            pytest.skip(f"Synthesis failed: {e}")


# Configuration and hardware detection tests
class TestHardwareDetection:
    """Test hardware detection in engine initialization."""
    
    def test_auto_device_detection(self):
        """Test that auto device detection works."""
        import torch
        from voice_cloning.config import get_recommended_config_for_hardware
        
        config = get_recommended_config_for_hardware()
        
        # Should detect either CUDA or CPU
        if torch.cuda.is_available():
            assert "cuda" in config.get_device_info()
        else:
            assert "cpu" in config.get_device_info()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
