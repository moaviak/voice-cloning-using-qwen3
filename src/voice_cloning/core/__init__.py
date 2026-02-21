"""
Core Voice Cloning Engine

Provides the VoiceCloningEngine class for voice cloning and synthesis operations.
"""

import torch
import numpy as np
from pathlib import Path
from typing import Union, Tuple, List, Optional, Dict, Any, TYPE_CHECKING
from qwen_tts import Qwen3TTSModel
import soundfile as sf

if TYPE_CHECKING:
    from voice_cloning.config import EngineConfig


class VoiceCloningEngine:
    """
    Engine for voice cloning using Qwen3-TTS-12Hz-1.7B-Base model.
    Supports GPU/CPU detection and automatic loading.
    """

    def __init__(
        self,
        model_path: Union[str, Path, "EngineConfig"] = None,
        device: Optional[str] = None,
        dtype: torch.dtype = torch.bfloat16,
        use_flash_attention: bool = False,
    ):
        """
        Initialize the Voice Cloning Engine.

        Args:
            model_path: Either an EngineConfig object OR path to the local Qwen3-TTS model directory.
                       Can be a string/Path for backward compatibility.
            device: Device to use ('cuda', 'cpu', or None for auto-detection).
                   Ignored if model_path is an EngineConfig object.
            dtype: Data type for model (torch.bfloat16 or torch.float32).
                  Ignored if model_path is an EngineConfig object.
            use_flash_attention: Whether to use Flash Attention 2 (requires GPU).
                                Ignored if model_path is an EngineConfig object.

        Raises:
            FileNotFoundError: If model path doesn't exist
            ValueError: If model configuration is invalid
        """
        # Handle EngineConfig object
        if hasattr(model_path, "model_path"):  # Check if it's an EngineConfig
            config = model_path
            self.model_path = Path(config.model_path)
            self.device = config.device if config.device else self._detect_device()
            self.dtype = config.dtype
            self.use_flash_attention = config.use_flash_attention
        else:
            # Handle string/Path model_path
            self.model_path = Path(model_path)
            
            # Auto-detect device if not specified
            if device is None:
                self.device = self._detect_device()
            else:
                self.device = device
            
            self.dtype = dtype
            self.use_flash_attention = use_flash_attention
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model path not found: {self.model_path}")
        
        self.model = None
        self.clone_prompts: Dict[str, Any] = {}
        self.sample_rate = 24000
        
        # Load model
        self._load_model()

    def _detect_device(self) -> str:
        """
        Auto-detect available device (GPU or CPU).

        Returns:
            Device string ('cuda:0' for GPU or 'cpu')
        """
        if torch.cuda.is_available():
            cuda_device = torch.cuda.current_device()
            device_name = torch.cuda.get_device_name(cuda_device)
            print(f"✓ GPU detected: {device_name}")
            return f"cuda:{cuda_device}"
        else:
            print("✓ No GPU available - using CPU for inference")
            print("  Note: CPU inference will be slower than GPU")
            return "cpu"

    def _load_model(self) -> None:
        """
        Load the Qwen3-TTS model from local path.

        Raises:
            RuntimeError: If model loading fails
        """
        try:
            print(f"\nLoading Qwen3-TTS model from: {self.model_path}")
            print(f"Device: {self.device}")
            print(f"DType: {self.dtype}")
            
            # Prepare loading kwargs
            load_kwargs = {
                "device_map": self.device,
                "dtype": self.dtype,
            }
            
            # Add flash attention if specified and on GPU
            if self.use_flash_attention and "cuda" in self.device:
                load_kwargs["attn_implementation"] = "flash_attention_2"
                print("Using Flash Attention 2")
            
            # Load the model
            self.model = Qwen3TTSModel.from_pretrained(
                str(self.model_path),
                **load_kwargs
            )
            
            print("✓ Model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def create_voice_clone_prompt(
        self,
        audio_path: Union[str, Path],
        transcript: str,
        prompt_name: Optional[str] = None,
        x_vector_only_mode: bool = False,
    ) -> str:
        """
        Create a voice cloning prompt from audio file and its transcript.
        The prompt is cached internally for reuse.

        Args:
            audio_path: Path to the reference audio file (.wav)
            transcript: Text transcript of the audio content
            prompt_name: Optional name to store this prompt for later reuse.
                        If None, generates a name from audio filename.
            x_vector_only_mode: If True, only uses speaker embedding (reduced quality).
                               Set False for better cloning quality.

        Returns:
            Prompt identifier (can be used to reference this prompt later)

        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio file is invalid
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Generate prompt name if not provided
        if prompt_name is None:
            prompt_name = audio_path.stem
        
        print(f"\nCreating voice clone prompt: {prompt_name}")
        print(f"  Audio: {audio_path}")
        print(f"  Transcript: {transcript[:100]}...")
        
        try:
            # Create the voice clone prompt from audio and transcript
            prompt_items = self.model.create_voice_clone_prompt(
                ref_audio=str(audio_path),
                ref_text=transcript,
                x_vector_only_mode=x_vector_only_mode,
            )
            
            # Cache the prompt
            self.clone_prompts[prompt_name] = prompt_items
            
            print(f"✓ Voice clone prompt created successfully!")
            
            return prompt_name
            
        except Exception as e:
            raise ValueError(f"Failed to create voice clone prompt: {str(e)}")

    def synthesize_voice(
        self,
        text: Union[str, List[str]],
        language: Union[str, List[str]] = "Auto",
        prompt_name: Optional[str] = None,
        voice_clone_prompt: Optional[Any] = None,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Tuple[np.ndarray, int]:
        """
        Synthesize speech using a voice clone prompt.

        Args:
            text: Text to synthesize (single string or list of strings for batch)
            language: Language(s) for synthesis. "Auto" for auto-detection.
                     Can be "Chinese", "English", "Japanese", "Korean", "German",
                     "French", "Russian", "Portuguese", "Spanish", or "Italian"
            prompt_name: Name of a cached prompt to use (created with create_voice_clone_prompt)
            voice_clone_prompt: Direct prompt object (alternative to prompt_name)
            output_path: Optional path to save the output audio file

        Returns:
            Tuple of (audio_waveform, sample_rate)
            - audio_waveform: numpy array of audio samples
            - sample_rate: audio sample rate (typically 24000)

        Raises:
            ValueError: If prompt not found or synthesis fails
        """
        # Validate prompt
        if voice_clone_prompt is None and prompt_name is None:
            raise ValueError("Either prompt_name or voice_clone_prompt must be provided")
        
        # Get prompt object
        if voice_clone_prompt is None:
            if prompt_name not in self.clone_prompts:
                available = list(self.clone_prompts.keys())
                raise ValueError(
                    f"Prompt '{prompt_name}' not found. "
                    f"Available prompts: {available}"
                )
            voice_clone_prompt = self.clone_prompts[prompt_name]
        
        # Prepare language parameter
        if isinstance(text, str):
            is_single = True
            languages = language
        else:
            is_single = False
            languages = language if isinstance(language, list) else [language] * len(text)
        
        print(f"\nSynthesizing voice...")
        print(f"  Using prompt: {prompt_name}")
        
        try:
            # Generate voice clone
            wavs, sr = self.model.generate_voice_clone(
                text=text,
                language=languages,
                voice_clone_prompt=voice_clone_prompt,
            )
            
            print(f"✓ Voice synthesis completed!")
            print(f"  Sample rate: {sr} Hz")
            
            # Handle single vs batch output
            if is_single:
                audio = wavs[0] if isinstance(wavs, list) else wavs
            else:
                audio = wavs
            
            # Save to file if path provided
            if output_path is not None:
                self._save_audio(audio, sr, output_path, is_batch=not is_single)
            
            return audio, sr
            
        except Exception as e:
            raise ValueError(f"Failed to synthesize voice: {str(e)}")

    def synthesize_and_save(
        self,
        text: Union[str, List[str]],
        output_path: Union[str, Path],
        language: Union[str, List[str]] = "Auto",
        prompt_name: Optional[str] = None,
        voice_clone_prompt: Optional[Any] = None,
    ) -> Path:
        """
        Synthesize speech and save directly to file(s).

        Args:
            text: Text to synthesize
            output_path: Output file path (or directory for batch output)
            language: Language(s) for synthesis
            prompt_name: Name of cached prompt
            voice_clone_prompt: Direct prompt object

        Returns:
            Path(s) to saved file(s)
        """
        audio, sr = self.synthesize_voice(
            text=text,
            language=language,
            prompt_name=prompt_name,
            voice_clone_prompt=voice_clone_prompt,
            output_path=output_path,
        )
        return output_path

    def _save_audio(
        self,
        audio: Union[np.ndarray, List[np.ndarray]],
        sr: int,
        output_path: Union[str, Path],
        is_batch: bool = False,
    ) -> None:
        """
        Save audio to file(s).

        Args:
            audio: Audio waveform(s)
            sr: Sample rate
            output_path: Output file path
            is_batch: Whether this is batch output
        """
        output_path = Path(output_path)
        
        if is_batch:
            # Batch output - create directory if needed
            output_dir = output_path.parent if output_path.suffix else output_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, wav in enumerate(audio):
                file_path = output_dir / f"output_{i}.wav"
                sf.write(str(file_path), wav, sr)
                print(f"  Saved: {file_path}")
        else:
            # Single output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sf.write(str(output_path), audio, sr)
            print(f"  Saved: {output_path}")

    def list_cached_prompts(self) -> List[str]:
        """
        Get list of all cached voice clone prompts.

        Returns:
            List of prompt names
        """
        return list(self.clone_prompts.keys())

    def clear_prompt_cache(self, prompt_name: Optional[str] = None) -> None:
        """
        Clear cached prompts to free memory.

        Args:
            prompt_name: Specific prompt to clear. If None, clears all.
        """
        if prompt_name is None:
            self.clone_prompts.clear()
            print("✓ All prompts cleared")
        elif prompt_name in self.clone_prompts:
            del self.clone_prompts[prompt_name]
            print(f"✓ Prompt '{prompt_name}' cleared")
        else:
            print(f"Warning: Prompt '{prompt_name}' not found")

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages.

        Returns:
            List of language names
        """
        return [
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
        ]

    def __repr__(self) -> str:
        """String representation of the engine."""
        return (
            f"VoiceCloningEngine(\n"
            f"  model_path={self.model_path}\n"
            f"  device={self.device}\n"
            f"  dtype={self.dtype}\n"
            f"  cached_prompts={len(self.clone_prompts)}\n"
            f")"
        )
