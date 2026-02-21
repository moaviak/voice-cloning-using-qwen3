from huggingface_hub import snapshot_download
import os

# Configuration
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"  # Replace with your specific Qwen model
SAVE_PATH = "../models/qwen3-tts"

print(f"Starting download for {MODEL_ID}...")

try:
    path = snapshot_download(
        repo_id=MODEL_ID,
        local_dir=SAVE_PATH,
        local_dir_use_symlinks=False, # This ensures actual files are copied, not links
        revision="main"
    )
    print(f"Successfully downloaded to: {os.path.abspath(path)}")
except Exception as e:
    print(f"An error occurred: {e}")