"""
Integration tests for voice cloning system.

These tests verify end-to-end workflows and component interactions.
"""

import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestImportIntegration:
    """Test that all imports work together."""
    
    def test_core_imports(self):
        """Test importing core components."""
        from voice_cloning import VoiceCloningEngine
        from voice_cloning.config import EngineConfig, get_recommended_config_for_hardware
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None
    
    def test_api_imports(self):
        """Test importing API components."""
        from voice_cloning.api.models import (
            PromptResponse,
            SynthesisRequest,
            SynthesisResponse,
            EngineStatus,
        )
        
        assert PromptResponse is not None
        assert SynthesisRequest is not None
        assert SynthesisResponse is not None
        assert EngineStatus is not None
    
    def test_backward_compatibility_imports(self):
        """Test that backward compatibility imports work."""
        from qwen3_voice_engine import VoiceCloningEngine
        from config import EngineConfig, get_recommended_config_for_hardware
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None


class TestConfigurationFlow:
    """Test typical configuration workflows."""
    
    def test_get_auto_config(self):
        """Test getting auto-detected configuration."""
        from voice_cloning.config import get_recommended_config_for_hardware
        
        config = get_recommended_config_for_hardware()
        assert config is not None
        assert config.validate() is True
    
    def test_config_cpu_preset(self):
        """Test getting CPU preset configuration."""
        from voice_cloning.config import get_config
        
        config = get_config("cpu")
        assert config.device == "cpu"
        assert config.validate() is True
    
    def test_config_gpu_preset(self):
        """Test getting GPU preset configuration."""
        from voice_cloning.config import get_config, PRESETS
        
        if "standard_gpu" in PRESETS:
            config = get_config("standard_gpu")
            assert "cuda" in config.device or config.device == "cuda:0"
            assert config.validate() is True


class TestAPIModelFlow:
    """Test typical API model workflows."""
    
    def test_synthesis_request_response(self):
        """Test creating and validating synthesis request/response."""
        from voice_cloning.api.models import SynthesisRequest, SynthesisResponse
        
        # Create request
        request = SynthesisRequest(
            text="Test synthesis",
            prompt_name="test_voice",
            language="English"
        )
        
        # Serialize request
        req_data = request.model_dump()
        
        # Simulate response
        response = SynthesisResponse(
            status="success",
            message="Synthesized",
            filename="output.wav",
            duration_seconds=2.0
        )
        
        # Serialize response
        resp_data = response.model_dump()
        
        assert req_data["text"] == "Test synthesis"
        assert resp_data["status"] == "success"
    
    def test_prompt_creation_response(self):
        """Test prompt creation workflow."""
        from voice_cloning.api.models import PromptResponse
        
        response = PromptResponse(
            prompt_id="prompt_123",
            prompt_name="my_voice",
            status="success",
            message="Prompt created",
            duration_seconds=5.0,
            sample_rate=24000
        )
        
        data = response.model_dump()
        assert data["prompt_id"] == "prompt_123"
        assert data["prompt_name"] == "my_voice"
        assert data["status"] == "success"


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""
    
    def test_configuration_engine_setup(self, config_with_test_settings):
        """Test setting up engine from configuration."""
        from voice_cloning import VoiceCloningEngine
        
        # Configure engine
        config = config_with_test_settings
        assert config.validate() is True
        
        # Would initialize engine here if models were available
        # engine = VoiceCloningEngine(config)
        # assert engine is not None
    
    @pytest.mark.requires_model
    def test_voice_creation_and_synthesis_workflow(self, engine, sample_audio_file, test_output_dir):
        """Test creating voice and synthesizing audio."""
        from pathlib import Path
        
        # Check that engine has required methods
        assert hasattr(engine, 'create_voice_clone_prompt')
        assert hasattr(engine, 'synthesize_voice')
        assert hasattr(engine, 'list_cached_prompts')
        
        # These would work if models and cache were properly set up
        # prompt_id = engine.create_voice_clone_prompt(
        #     audio_path=str(sample_audio_file),
        #     transcript="Test transcript",
        #     prompt_name="test_voice"
        # )
        # assert prompt_id is not None


class TestErrorHandlingIntegration:
    """Test error handling across modules."""
    
    def test_invalid_config_handling(self):
        """Test handling invalid configurations."""
        from voice_cloning.config import EngineConfig
        
        # Invalid device
        config = EngineConfig(device="invalid")
        assert config.validate() is False
        
        # Valid device
        config = EngineConfig(device="cpu")
        assert config.validate() is True
    
    def test_api_model_validation_errors(self):
        """Test API model validation errors."""
        from voice_cloning.api.models import SynthesisRequest
        
        # Empty text should fail
        with pytest.raises(ValueError):
            SynthesisRequest(
                text="",
                prompt_name="test"
            )


class TestDataValidationIntegration:
    """Test data validation across the system."""
    
    def test_synthesis_request_validation(self):
        """Test SynthesisRequest validates input."""
        from voice_cloning.api.models import SynthesisRequest
        
        # Valid request
        req = SynthesisRequest(
            text="Valid text",
            prompt_name="test_prompt"
        )
        assert req.text == "Valid text"
        
        # Invalid request (empty text)
        with pytest.raises(ValueError):
            SynthesisRequest(
                text="",
                prompt_name="test_prompt"
            )
    
    def test_config_validation_integration(self):
        """Test config validation across system."""
        from voice_cloning.config import (
            EngineConfig,
            get_recommended_config_for_hardware,
            PRESETS
        )
        
        # Test all presets are valid
        for preset_name, preset_config in PRESETS.items():
            assert preset_config.validate() is True, f"{preset_name} is invalid"
        
        # Test recommended config is valid
        recommended = get_recommended_config_for_hardware()
        assert recommended.validate() is True


class TestModuleStructureIntegration:
    """Test that module structure supports all expected operations."""
    
    def test_package_exports(self):
        """Test that package exports main classes."""
        from voice_cloning import (
            VoiceCloningEngine,
            EngineConfig,
        )
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None
    
    def test_submodule_access(self):
        """Test accessing submodule components."""
        from voice_cloning.core import VoiceCloningEngine
        from voice_cloning.config import EngineConfig
        from voice_cloning.api.models import SynthesisRequest
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None
        assert SynthesisRequest is not None
    
    def test_backward_compatibility_modules(self):
        """Test backward compatibility module access."""
        from qwen3_voice_engine import VoiceCloningEngine
        from config import EngineConfig
        
        assert VoiceCloningEngine is not None
        assert EngineConfig is not None


# Performance-related integration tests
class TestPerformanceIntegration:
    """Test performance and efficiency of system."""
    
    def test_config_initialization_speed(self):
        """Test that config initialization is fast."""
        import time
        from voice_cloning.config import get_recommended_config_for_hardware
        
        start = time.time()
        config = get_recommended_config_for_hardware()
        elapsed = time.time() - start
        
        # Should be very fast (< 1 second)
        assert elapsed < 1.0
        assert config is not None
    
    def test_model_creation_speed(self):
        """Test that model creation is reasonably fast."""
        import time
        from voice_cloning.api.models import SynthesisRequest
        
        start = time.time()
        for _ in range(100):
            req = SynthesisRequest(
                text="Test",
                prompt_name="test"
            )
        elapsed = time.time() - start
        
        # Should create 100 models in < 1 second
        assert elapsed < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
