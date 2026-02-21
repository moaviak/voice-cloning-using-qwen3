"""
REST API Client Example

This example shows how to interact with the Voice Cloning API server
using the requests library.

Demonstrates:
1. Starting the API server
2. Creating a voice clone via API
3. Synthesizing audio via API
4. Managing the API client

Requirements:
- API server running (python scripts/run_api.py)
- requests library (pip install requests)
"""

import requests
import time
from pathlib import Path
from typing import Optional


class VoiceCloningAPIClient:
    """Client for interacting with Voice Cloning API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip("/")
        self.api_version = "v1"
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to API.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response JSON as dictionary
        """
        url = f"{self.base_url}/api/{self.api_version}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.text else {"status": "success"}
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Failed to connect to {self.base_url}. Is the server running?")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"API Error: {e.response.status_code} - {e.response.text}")
    
    def check_health(self) -> dict:
        """Check API server health and status.
        
        Returns:
            Server status information
        """
        return self._make_request("GET", "/health")
    
    def create_voice_clone(
        self, 
        audio_file: str, 
        transcript: str, 
        prompt_name: str
    ) -> dict:
        """Create a voice clone from audio and transcript.
        
        Args:
            audio_file: Path to .wav audio file
            transcript: Text transcript of the audio
            prompt_name: Name to store the voice prompt as
            
        Returns:
            Response with prompt ID and metadata
        """
        if not Path(audio_file).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Read file content and send with proper content type
        with open(audio_file, "rb") as f:
            files = {"audio": (Path(audio_file).name, f, "audio/wav")}
            data = {"transcript": transcript, "prompt_name": prompt_name}
            url = f"{self.base_url}/api/{self.api_version}/create-prompt"
            
            try:
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                return response.json() if response.text else {"status": "success"}
            except requests.exceptions.HTTPError as e:
                raise RuntimeError(f"API Error: {e.response.status_code} - {e.response.text}")
    
    def synthesize_audio(
        self,
        text: str,
        prompt_name: str,
        language: str = "Auto"
    ) -> bytes:
        """Synthesize audio using a voice clone.
        
        Args:
            text: Text to synthesize
            prompt_name: Name of the voice prompt to use
            language: Language for synthesis
            
        Returns:
            Audio data as bytes
        """
        payload = {
            "text": text,
            "prompt_name": prompt_name,
            "language": language
        }
        
        response = requests.post(
            f"{self.base_url}/api/{self.api_version}/synthesize",
            json=payload
        )
        response.raise_for_status()
        
        return response.content
    
    def list_prompts(self) -> dict:
        """List all cached voice prompts.
        
        Returns:
            List of cached prompts with metadata
        """
        return self._make_request("GET", "/prompts")
    
    def delete_prompt(self, prompt_id: str) -> dict:
        """Delete a specific voice prompt.
        
        Args:
            prompt_id: ID of the prompt to delete
            
        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/prompts/{prompt_id}")
    
    def download_audio(self, filename: str, output_path: Optional[str] = None) -> str:
        """Download synthesized audio file.
        
        Args:
            filename: Name of the file to download
            output_path: Path to save file (optional)
            
        Returns:
            Path to downloaded file
        """
        url = f"{self.base_url}/api/{self.api_version}/download/{filename}"
        response = requests.get(url)
        response.raise_for_status()
        
        if output_path is None:
            output_path = filename
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path


def main():
    """Main example function."""
    
    print("=" * 70)
    print("Voice Cloning API Client - Usage Example")
    print("=" * 70)
    
    # Initialize client
    client = VoiceCloningAPIClient(base_url="http://localhost:8000")
    
    print("\n[1/4] Checking API server health...")
    try:
        status = client.check_health()
        print(f"✓ Server is healthy")
        print(f"  Device: {status.get('device', 'N/A')}")
        print(f"  Model: {status.get('model', 'N/A')}")
        print(f"  Cached prompts: {status.get('cached_prompts_count', 0)}")
    except ConnectionError as e:
        print(f"✗ {e}")
        print("\nTo start the API server, run:")
        print("  python scripts/run_api.py")
        return
    
    # Setup sample audio and transcript
    sample_audio = Path(__file__).parent / "sample_audios" / "1.wav"
    transcript = (
        "Please call Stella. Ask her to bring these things with her from the store: "
        "Six spoons of fresh snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob. "
        "We also need a small plastic snake and a big toy frog for the kids. "
        "She can scoop these things into three red bags, and we will go meet her Wednesday at the train station."
    )
    
    print("\n[2/4] Creating voice clone...")
    if not sample_audio.exists():
        print(f"✗ Sample audio not found at: {sample_audio}")
        print("  Please ensure the sample_audios/1.wav file exists.")
        return
    
    print(f"  Audio file: {sample_audio}")
    print(f"  Transcript: {transcript[:60]}...")
    
    try:
        response = client.create_voice_clone(
            audio_file=str(sample_audio),
            transcript=transcript,
            prompt_name="api_sample_voice"
        )
        print(f"✓ Voice clone created successfully")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"✗ Error creating voice clone: {e}")
        return
    
    print("\n[3/4] Listing cached prompts...")
    try:
        prompts = client.list_prompts()
        print(f"✓ Cached prompts retrieved")
        print(f"  Prompts: {prompts}")
    except Exception as e:
        print(f"✗ Error listing prompts: {e}")
    
    print("\n[4/4] Synthesizing audio...")
    synthesis_texts = [
        "Hello from the API voice cloning system.",
        "This audio was generated using a cloned voice.",
        "The voice was created from the sample audio file."
    ]
    
    output_dir = Path("api_output")
    output_dir.mkdir(exist_ok=True)
    
    for i, text in enumerate(synthesis_texts, 1):
        try:
            print(f"  [{i}/{len(synthesis_texts)}] Synthesizing: {text[:40]}...")
            audio_data = client.synthesize_audio(
                text=text,
                prompt_name="api_sample_voice",
                language="English"
            )
            
            output_path = output_dir / f"api_output_{i:02d}.wav"
            with open(output_path, "wb") as f:
                f.write(audio_data)
            
            print(f"    ✓ Saved to: {output_path}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("API Endpoints Available:")
    print("=" * 70)
    print("\n  POST   /api/v1/create-prompt  - Create voice clone")
    print("  POST   /api/v1/synthesize     - Synthesize audio")
    print("  GET    /api/v1/download/{i}   - Download audio file")
    print("  GET    /api/v1/prompts        - List cached prompts")
    print("  DELETE /api/v1/prompts/{id}   - Delete prompt")
    print("  GET    /api/v1/health         - Check server status")
    
    print("\n" + "=" * 70)
    print("Starting API Server:")
    print("=" * 70)
    print("\n  python scripts/run_api.py --port 8000 --reload")
    print("\n  Optional arguments:")
    print("    --port PORT        Server port (default: 8000)")
    print("    --workers N        Number of workers (default: 1)")
    print("    --reload           Auto-reload on code changes")
    print("    --log-level LEVEL  Log level (debug, info, warning, error)")


if __name__ == "__main__":
    main()
