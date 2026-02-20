"""
Unit tests for voice_cloning.api module.

Tests API endpoints, models, and request/response handling.
"""

import sys
from pathlib import Path
import pytest
from io import BytesIO

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_cloning.api.models import (
    PromptResponse,
    SynthesisRequest,
    SynthesisResponse,
    EngineStatus,
)


class TestPromptResponse:
    """Test PromptResponse model."""
    
    def test_prompt_response_creation(self):
        """Test creating PromptResponse."""
        response = PromptResponse(
            prompt_id="test_123",
            prompt_name="test_voice",
            status="success",
            message="Voice prompt created successfully"
        )
        
        assert response.prompt_id == "test_123"
        assert response.prompt_name == "test_voice"
        assert response.status == "success"
        assert response.message == "Voice prompt created successfully"
    
    def test_prompt_response_with_optional_fields(self):
        """Test PromptResponse with optional fields."""
        response = PromptResponse(
            prompt_id="test_123",
            prompt_name="test_voice",
            status="success",
            message="Success",
            duration_seconds=5.2,
            sample_rate=24000
        )
        
        assert response.duration_seconds == 5.2
        assert response.sample_rate == 24000
    
    def test_prompt_response_model_dump(self):
        """Test PromptResponse model serialization."""
        response = PromptResponse(
            prompt_id="test_123",
            prompt_name="test_voice",
            status="success",
            message="Success"
        )
        
        data = response.model_dump()
        assert isinstance(data, dict)
        assert data["prompt_id"] == "test_123"
        assert data["prompt_name"] == "test_voice"


class TestSynthesisRequest:
    """Test SynthesisRequest model."""
    
    def test_synthesis_request_creation(self):
        """Test creating SynthesisRequest."""
        request = SynthesisRequest(
            text="Hello world",
            prompt_name="test_voice",
            language="English"
        )
        
        assert request.text == "Hello world"
        assert request.prompt_name == "test_voice"
        assert request.language == "English"
    
    def test_synthesis_request_with_defaults(self):
        """Test SynthesisRequest with default language."""
        request = SynthesisRequest(
            text="Hello world",
            prompt_name="test_voice"
        )
        
        # Default should be "Auto"
        assert request.language == "Auto"
    
    def test_synthesis_request_validation(self):
        """Test SynthesisRequest validation."""
        # Empty text should be invalid
        with pytest.raises(ValueError):
            SynthesisRequest(
                text="",
                prompt_name="test_voice"
            )
    
    def test_synthesis_request_model_dump(self):
        """Test SynthesisRequest serialization."""
        request = SynthesisRequest(
            text="Hello world",
            prompt_name="test_voice",
            language="English"
        )
        
        data = request.model_dump()
        assert isinstance(data, dict)
        assert data["text"] == "Hello world"
        assert data["prompt_name"] == "test_voice"
        assert data["language"] == "English"


class TestSynthesisResponse:
    """Test SynthesisResponse model."""
    
    def test_synthesis_response_creation(self):
        """Test creating SynthesisResponse."""
        response = SynthesisResponse(
            status="success",
            message="Audio synthesized successfully",
            filename="output_123.wav",
            duration_seconds=2.5
        )
        
        assert response.status == "success"
        assert response.filename == "output_123.wav"
        assert response.duration_seconds == 2.5
    
    def test_synthesis_response_with_url(self):
        """Test SynthesisResponse with download URL."""
        response = SynthesisResponse(
            status="success",
            message="Success",
            filename="output_123.wav",
            duration_seconds=2.5,
            download_url="http://localhost:8000/api/v1/download/output_123.wav"
        )
        
        assert response.download_url is not None
        assert "download" in response.download_url
    
    def test_synthesis_response_model_dump(self):
        """Test SynthesisResponse serialization."""
        response = SynthesisResponse(
            status="success",
            message="Success",
            filename="output_123.wav",
            duration_seconds=2.5
        )
        
        data = response.model_dump()
        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert data["filename"] == "output_123.wav"


class TestEngineStatus:
    """Test EngineStatus model."""
    
    def test_engine_status_creation(self):
        """Test creating EngineStatus."""
        status = EngineStatus(
            device="cuda:0",
            model="qwen3-tts",
            cached_prompts_count=2,
            status="ready"
        )
        
        assert status.device == "cuda:0"
        assert status.model == "qwen3-tts"
        assert status.cached_prompts_count == 2
        assert status.status == "ready"
    
    def test_engine_status_cpu_device(self):
        """Test EngineStatus with CPU device."""
        status = EngineStatus(
            device="cpu",
            model="qwen3-tts",
            cached_prompts_count=0,
            status="ready"
        )
        
        assert status.device == "cpu"
    
    def test_engine_status_model_dump(self):
        """Test EngineStatus serialization."""
        status = EngineStatus(
            device="cuda:0",
            model="qwen3-tts",
            cached_prompts_count=2,
            status="ready"
        )
        
        data = status.model_dump()
        assert isinstance(data, dict)
        assert data["device"] == "cuda:0"
        assert data["model"] == "qwen3-tts"
        assert data["cached_prompts_count"] == 2
        assert data["status"] == "ready"


class TestAPIModelsValidation:
    """Test validation of API models."""
    
    def test_synthesis_request_language_validation(self):
        """Test that SynthesisRequest validates language parameter."""
        # Valid language
        request = SynthesisRequest(
            text="Hello",
            prompt_name="test",
            language="English"
        )
        assert request.language == "English"
        
        # Auto should be valid
        request = SynthesisRequest(
            text="Hello",
            prompt_name="test",
            language="Auto"
        )
        assert request.language == "Auto"
    
    def test_prompt_response_status_values(self):
        """Test PromptResponse status values."""
        success_response = PromptResponse(
            prompt_id="test",
            prompt_name="test",
            status="success",
            message="OK"
        )
        assert success_response.status == "success"
        
        error_response = PromptResponse(
            prompt_id="test",
            prompt_name="test",
            status="error",
            message="Failed"
        )
        assert error_response.status == "error"


# Integration-style tests
class TestAPIModelsIntegration:
    """Integration tests for API models."""
    
    def test_request_response_flow(self):
        """Test typical request-response flow."""
        # Create request
        request = SynthesisRequest(
            text="Test synthesis",
            prompt_name="test_voice",
            language="English"
        )
        
        # Simulate response
        response = SynthesisResponse(
            status="success",
            message="Synthesis completed",
            filename="output.wav",
            duration_seconds=2.0
        )
        
        # Verify round-trip
        request_data = request.model_dump()
        response_data = response.model_dump()
        
        assert request_data["text"] == "Test synthesis"
        assert response_data["status"] == "success"
    
    def test_error_response(self):
        """Test error response creation."""
        error_response = PromptResponse(
            prompt_id="",
            prompt_name="",
            status="error",
            message="Failed to process audio file"
        )
        
        assert error_response.status == "error"
        assert "Failed" in error_response.message


# JSON serialization tests
class TestAPIPydanticSerializability:
    """Test that API models can be serialized to JSON."""
    
    def test_prompt_response_json(self):
        """Test PromptResponse JSON serialization."""
        response = PromptResponse(
            prompt_id="test_123",
            prompt_name="test_voice",
            status="success",
            message="Created"
        )
        
        json_str = response.model_dump_json()
        assert isinstance(json_str, str)
        assert '"prompt_id":"test_123"' in json_str or '"prompt_id": "test_123"' in json_str
    
    def test_synthesis_response_json(self):
        """Test SynthesisResponse JSON serialization."""
        response = SynthesisResponse(
            status="success",
            message="Success",
            filename="out.wav",
            duration_seconds=1.5
        )
        
        json_str = response.model_dump_json()
        assert isinstance(json_str, str)
        assert "success" in json_str
        assert "out.wav" in json_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
