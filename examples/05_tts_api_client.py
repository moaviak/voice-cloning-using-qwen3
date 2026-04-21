"""
TTS API Client Example

This example tests the custom voice TTS endpoint:
POST /api/v1/tts

Requirements:
- API server running (python scripts/run_api.py)
- requests library (pip install requests)
"""

from pathlib import Path

import requests


def generate_tts(
    base_url: str,
    text: str,
    speaker: str = "aiden",
    language: str = "english",
) -> bytes:
    """Call TTS endpoint and return WAV bytes."""
    payload = {
        "text": text,
        "speaker": speaker,
        "language": language,
    }
    response = requests.post(f"{base_url}/api/v1/tts", json=payload)
    response.raise_for_status()
    return response.content


def main() -> None:
    base_url = "http://localhost:8000"
    output_dir = Path("api_output")
    output_dir.mkdir(exist_ok=True)

    tests = [
        {"text": "Hello, this is a custom voice test.", "speaker": "aiden", "language": "english"},
        {"text": "This is a second sentence for verification.", "speaker": "aiden", "language": "english"},
    ]

    print("=" * 70)
    print("TTS API Client - Endpoint Test")
    print("=" * 70)
    print(f"Server: {base_url}")
    print("Endpoint: POST /api/v1/tts")

    for idx, item in enumerate(tests, 1):
        try:
            print(f"\n[{idx}/{len(tests)}] Generating TTS...")
            print(f"  Text: {item['text']}")
            print(f"  Speaker: {item['speaker']}")
            print(f"  Language: {item['language']}")

            wav_bytes = generate_tts(
                base_url=base_url,
                text=item["text"],
                speaker=item["speaker"],
                language=item["language"],
            )

            output_path = output_dir / f"tts_output_{idx:02d}.wav"
            output_path.write_bytes(wav_bytes)
            print(f"  ✓ Saved: {output_path}")
        except requests.exceptions.ConnectionError:
            print("  ✗ Failed to connect. Start server with: python scripts/run_api.py")
            return
        except requests.exceptions.HTTPError as exc:
            print(f"  ✗ API Error: {exc.response.status_code} - {exc.response.text}")
        except Exception as exc:
            print(f"  ✗ Unexpected error: {exc}")

    print("\nDone. Check generated files in api_output/.")


if __name__ == "__main__":
    main()
