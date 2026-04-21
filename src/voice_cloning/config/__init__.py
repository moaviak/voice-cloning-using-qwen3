"""
Configuration module for Voice Cloning Engine.

Provides configuration classes, preset configurations, and hardware detection.
"""

import torch
from dataclasses import dataclass
from typing import Optional


@dataclass
class EngineConfig:
    """Configuration for VoiceCloningEngine."""

    # Model Configuration
    model_path: str = "models/voice-cloning-model"
    """Path to the voice cloning model directory."""

    # Device Configuration
    device: Optional[str] = None
    """Device to use: 'cuda:0', 'cpu', or None for auto-detection."""

    auto_detect_device: bool = True
    """Automatically detect and use GPU if available."""

    # Data Type Configuration
    dtype: torch.dtype = torch.bfloat16
    """Data type for model inference.
    
    Options:
    - torch.bfloat16: Faster on GPU, lower memory (default, recommended for GPU)
    - torch.float32: Better CPU compatibility, slower on GPU
    """

    # Optimization Configuration
    use_flash_attention: bool = False
    """Enable Flash Attention 2 for faster GPU inference.
    Requires: CUDA GPU + flash_attn package installation.
    """

    enable_cpu_fallback: bool = True
    """Automatically fall back to CPU if GPU runs out of memory."""

    # Voice Cloning Configuration
    x_vector_only_mode: bool = False
    """Use only speaker embedding for voice cloning.
    
    Options:
    - False: Best quality (uses speaker + content info)
    - True: Faster but lower quality (speaker only)
    """

    # Audio Configuration
    sample_rate: int = 24000
    """Audio sample rate in Hz. Fixed at 24000 for the speech model."""

    default_language: str = "Auto"
    """Default language for text-to-speech synthesis.
    Set to 'Auto' for automatic language detection.
    """

    # Memory Configuration
    max_cached_prompts: int = 5
    """Maximum number of voice prompts to keep in memory.
    Set to 0 for unlimited (may cause memory issues)."""

    # Output Configuration
    output_dir: str = "output"
    """Directory to save synthesized audio files."""

    create_output_dir: bool = True
    """Automatically create output directory if it doesn't exist."""

    # Logging Configuration
    verbose: bool = True
    """Enable verbose logging."""

    log_file: Optional[str] = None
    """Optional log file path (None = no file logging)."""

    # Performance Configuration
    batch_size: int = 1
    """Default batch size for batch synthesis operations."""

    # Preset name
    preset: str = "auto"
    """Preset configuration name (for tracking which preset was used)."""

    # Supported Languages (read-only)
    supported_languages: tuple = (
        "Auto",
        "Chinese",
        "English",
        "Japanese",
        "Korean",
        "German",
        "French",
        "Russian",
        "Portuguese",
        "Spanish",
        "Italian",
    )
    """Languages supported by the speech model."""

    def validate(self) -> bool:
        """Validate configuration settings."""
        errors = []

        # Validate device
        if self.device is not None:
            if not (self.device.startswith("cuda") or self.device == "cpu"):
                errors.append(f"Invalid device: {self.device}")

        # Validate dtype
        if self.dtype not in [torch.bfloat16, torch.float32]:
            errors.append(f"Invalid dtype: {self.dtype}")

        # Validate language
        if self.default_language not in self.supported_languages:
            errors.append(f"Invalid default language: {self.default_language}")

        # Validate batch size
        if self.batch_size < 1:
            errors.append("batch_size must be >= 1")

        if errors:
            for error in errors:
                print(f"Config Error: {error}")
            return False

        return True

    def get_device_info(self) -> str:
        """Get human-readable device information."""
        if self.device:
            return self.device

        try:
            if torch.cuda.is_available():
                return f"cuda:0 (auto-detect)"
            else:
                return "cpu (auto-detect)"
        except Exception:
            return "unknown"

    def __str__(self) -> str:
        """String representation of config."""
        return (
            f"EngineConfig(\n"
            f"  preset={self.preset}\n"
            f"  model_path={self.model_path}\n"
            f"  device={self.get_device_info()}\n"
            f"  dtype={self.dtype}\n"
            f"  flash_attention={self.use_flash_attention}\n"
            f"  sample_rate={self.sample_rate}\n"
            f"  output_dir={self.output_dir}\n"
            f")"
        )


# Default configuration instance
DEFAULT_CONFIG = EngineConfig()


# Preset configurations for common scenarios
PRESETS = {
    "high_performance_gpu": EngineConfig(
        preset="high_performance_gpu",
        device="cuda:0",
        dtype=torch.bfloat16,
        use_flash_attention=True,
        batch_size=4,
    ),
    "standard_gpu": EngineConfig(
        preset="standard_gpu",
        device="cuda:0",
        dtype=torch.bfloat16,
        use_flash_attention=False,
        batch_size=2,
    ),
    "low_vram_gpu": EngineConfig(
        preset="low_vram_gpu",
        device="cuda:0",
        dtype=torch.float32,
        use_flash_attention=False,
        batch_size=1,
    ),
    "cpu": EngineConfig(
        preset="cpu",
        device="cpu",
        dtype=torch.float32,
        use_flash_attention=False,
        batch_size=1,
    ),
    "auto": EngineConfig(preset="auto"),
}


def get_config(preset: str = "auto") -> EngineConfig:
    """
    Get a preset configuration.
    
    Args:
        preset: Configuration preset name
        
    Returns:
        EngineConfig instance
        
    Raises:
        ValueError: If preset name is invalid
    """
    if preset in PRESETS:
        return PRESETS[preset]
    else:
        available = list(PRESETS.keys())
        raise ValueError(f"Unknown preset: {preset}. Available: {available}")


def get_recommended_config_for_hardware() -> EngineConfig:
    """
    Get recommended configuration based on available hardware.
    
    Returns:
        EngineConfig optimized for current hardware
    """
    config = EngineConfig()

    # Check CUDA availability
    if torch.cuda.is_available():
        config.device = "cuda:0"
        config.dtype = torch.bfloat16
        config.preset = "standard_gpu"

        # Check VRAM
        try:
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            if vram_gb >= 20:
                config = get_config("high_performance_gpu")
            elif vram_gb < 8:
                print(f"Warning: {vram_gb:.1f} GB VRAM detected. Using float32.")
                config = get_config("low_vram_gpu")
        except Exception:
            pass

    else:
        config = get_config("cpu")
        print("No GPU detected. Using CPU (slower inference).")

    return config


def load_config_from_file(config_file: str) -> EngineConfig:
    """
    Load configuration from a YAML or JSON file.
    
    Note: This is a placeholder for future implementation.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        EngineConfig instance
    """
    # TODO: Implement loading from config file
    return DEFAULT_CONFIG
