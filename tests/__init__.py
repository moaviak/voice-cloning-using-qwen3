"""
Voice Cloning Tests Package

This package contains comprehensive tests for the voice cloning system.

Test Structure:
- conftest.py: Pytest configuration and shared fixtures
- test_config.py: Configuration module tests
- test_api_models.py: API request/response model tests  
- test_engine.py: Core engine functionality tests
- test_integration.py: End-to-end integration tests

Running Tests:
--------------

Run all tests:
    pytest tests/ -v

Run specific test file:
    pytest tests/test_config.py -v

Run with markers:
    pytest -m "not slow"  # Skip slow tests
    pytest -m "not requires_gpu"  # Skip GPU tests
    pytest -m "requires_model"  # Only tests requiring models

Run with coverage:
    pytest tests/ --cov=src/voice_cloning --cov-report=html

Test Markers:
-------------
- @pytest.mark.slow: Tests that take > 1 minute
- @pytest.mark.requires_gpu: Tests that require GPU
- @pytest.mark.requires_model: Tests that require model files

Environment Variables:
----------------------
- SKIP_GPU_TESTS=1: Skip all GPU tests
- SKIP_SLOW_TESTS=1: Skip slow tests
"""

__all__ = [
    "test_config",
    "test_api_models", 
    "test_engine",
]
