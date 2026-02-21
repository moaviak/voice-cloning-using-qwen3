from huggingface_hub import snapshot_download
import os
from pathlib import Path

# Configuration
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"  # Replace with your specific Qwen model

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SAVE_PATH = PROJECT_ROOT / "models" / "qwen3-tts"

# Ensure the parent directory exists
SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"Starting download for {MODEL_ID}...")
print(f"Project root: {PROJECT_ROOT}")
print(f"Save path: {SAVE_PATH}")

try:
    path = snapshot_download(
        repo_id=MODEL_ID,
        local_dir=str(SAVE_PATH),
        local_dir_use_symlinks=False,  # This ensures actual files are copied, not links
        revision="main"
    )
    print(f"✓ Successfully downloaded to: {os.path.abspath(path)}")
except Exception as e:
    print(f"✗ An error occurred: {e}")