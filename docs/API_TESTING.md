# API Testing Guide

This guide provides ready-to-use test steps for the deployed API.

- Base URL: `http://13.61.4.1:8000`
- Swagger UI: `http://13.61.4.1:8000/api/docs`
- ReDoc: `http://13.61.4.1:8000/api/redoc`

## Quick Health Check

### Request
- Method: `GET`
- URL: `http://13.61.4.1:8000/api/v1/health`

### Expected
- Status: `200`
- JSON includes:
  - `status`
  - `device`
  - `dtype`
  - `model_loaded`
  - `cached_prompts`
  - `available_languages`

## Endpoint 1: Create Voice Prompt

Creates a reusable voice clone prompt from a reference WAV file and transcript.

### Request
- Method: `POST`
- URL: `http://13.61.4.1:8000/api/v1/create-prompt`
- Body type: `form-data`
  - `audio` (File): WAV file (`.wav`)
  - `transcript` (Text): transcript of uploaded audio
  - `prompt_name` (Text, optional): example `ahmed_voice`
  - `language` (Text, optional): example `English` (default is `Auto`)

### Expected
- Status: `200`
- JSON includes:
  - `prompt_id`
  - `prompt_name`
  - `voice_clone_prompt` (base64 string; use for synthesis)

## Endpoint 2: Synthesize Cloned Voice

Synthesizes speech using a `voice_clone_prompt` from `/create-prompt`.

### Request
- Method: `POST`
- URL: `http://13.61.4.1:8000/api/v1/synthesize`
- Headers:
  - `Content-Type: application/json`
- Body:

```json
{
  "text": "Hello, this is a synthesis test.",
  "language": "English",
  "voice_clone_prompt": "PASTE_FROM_CREATE_PROMPT_RESPONSE"
}
```

### Expected
- Status: `200`
- Response type: `audio/wav` stream
- Save response as a `.wav` file

## Endpoint 3: Custom TTS

Generates speech from text using the custom voice TTS model.

### Request
- Method: `POST`
- URL: `http://13.61.4.1:8000/api/v1/tts`
- Headers:
  - `Content-Type: application/json`
- Body:

```json
{
  "text": "Hello, this is a TTS test.",
  "speaker": "aiden",
  "language": "english"
}
```

### Expected
- Status: `200`
- Response type: `audio/wav` stream
- Save response as a `.wav` file

## Endpoint 4: List Prompts

### Request
- Method: `GET`
- URL: `http://13.61.4.1:8000/api/v1/prompts`

### Expected
- Status: `200`
- JSON with:
  - `success`
  - `count`
  - `prompts`

## Endpoint 5: Delete Prompt

### Request
- Method: `DELETE`
- URL: `http://13.61.4.1:8000/api/v1/prompts/{prompt_id}`

Replace `{prompt_id}` with value returned by `/create-prompt`.

### Expected
- Status: `200`
- JSON with success message

## Postman Testing Steps

1. Create a collection named `Voice Cloning API`.
2. Add collection variable:
   - `base_url = http://13.61.4.1:8000`
3. Create requests:
   - `GET {{base_url}}/api/v1/health`
   - `POST {{base_url}}/api/v1/create-prompt` (form-data)
   - `POST {{base_url}}/api/v1/synthesize` (raw JSON)
   - `POST {{base_url}}/api/v1/tts` (raw JSON)
   - `GET {{base_url}}/api/v1/prompts`
   - `DELETE {{base_url}}/api/v1/prompts/{prompt_id}`
4. For audio endpoints (`/synthesize`, `/tts`), use Postman "Send and Download" to save `.wav`.

## Common Errors

- `400 Invalid file format`: upload a real WAV file in `form-data` under key `audio`.
- `400 Invalid audio file. Could not decode WAV content.`: file extension may be `.wav` but content is invalid/non-WAV.
- `400 Text cannot be empty`: provide non-empty `text`.
- `404 Prompt not found`: use a valid `prompt_id` or pass `voice_clone_prompt`.
- `503 Engine not initialized` / `503 TTS model not initialized`: server started but model loading failed.
