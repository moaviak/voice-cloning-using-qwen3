import os
from pathlib import Path

from huggingface_hub import snapshot_download

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODELS_ROOT = PROJECT_ROOT / "models"

# Keep full model IDs here because they are required for downloading.
MODEL_DOWNLOADS = {
    "voice-cloning-model": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    "tts-model": "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
}


def download_model(target_dir: Path, model_id: str) -> None:
    """Download a model snapshot into the given target directory."""
    print(f"\nStarting download for {model_id}...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Save path: {target_dir}")

    path = snapshot_download(
        repo_id=model_id,
        local_dir=str(target_dir),
        local_dir_use_symlinks=False,  # Copy real files instead of symlinks.
        revision="main",
    )
    print(f"✓ Successfully downloaded to: {os.path.abspath(path)}")


def main() -> None:
    MODELS_ROOT.mkdir(parents=True, exist_ok=True)

    failures = []
    for folder_name, model_id in MODEL_DOWNLOADS.items():
        target_dir = MODELS_ROOT / folder_name
        try:
            download_model(target_dir=target_dir, model_id=model_id)
        except Exception as exc:
            failures.append((model_id, str(exc)))
            print(f"✗ Failed to download {model_id}: {exc}")

    if failures:
        print("\nCompleted with errors:")
        for model_id, error in failures:
            print(f"- {model_id}: {error}")
    else:
        print("\n✓ All model downloads completed successfully.")


if __name__ == "__main__":
    main()