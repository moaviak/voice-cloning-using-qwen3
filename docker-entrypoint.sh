#!/bin/bash
set -e

echo "═══════════════════════════════════════════"
echo "  Voice Cloning Engine — Startup"
echo "═══════════════════════════════════════════"

# ── 1. Define paths ──────────────────────────────────────────────
VOLUME_DIR="/runpod-volume"
MODEL_DIR="${VOLUME_DIR}/models"
VOICE_CLONE_MODEL="${MODEL_DIR}/voice-cloning-model"
TTS_MODEL="${MODEL_DIR}/tts-model"

# Symlink network volume models into /app/models so the app
# finds them at the path it expects (models/)
APP_MODEL_DIR="/app/models"

# ── 2. Check network volume is mounted ───────────────────────────
if [ ! -d "${VOLUME_DIR}" ]; then
    echo "⚠️  WARNING: Network volume not mounted at ${VOLUME_DIR}"
    echo "   Models will be downloaded to container disk (not persistent!)"
    MODEL_DIR="/app/models"
    VOICE_CLONE_MODEL="${MODEL_DIR}/voice-cloning-model"
    TTS_MODEL="${MODEL_DIR}/tts-model"
fi

# ── 3. Download models if not already present ────────────────────
mkdir -p "${MODEL_DIR}"

if [ ! -d "${VOICE_CLONE_MODEL}" ] || [ ! -f "${VOICE_CLONE_MODEL}/config.json" ]; then
    echo "📥 Models not found on volume. Downloading..."
    echo "   This only happens once. Future pod starts will skip this."
    python scripts/download_model.py \
        --voice-cloning-model-dir "${VOICE_CLONE_MODEL}" \
        --tts-model-dir "${TTS_MODEL}"
    echo "✅ Models downloaded to ${MODEL_DIR}"
else
    echo "✅ Models found on volume — skipping download."
    echo "   voice-cloning-model: ${VOICE_CLONE_MODEL}"
    echo "   tts-model:           ${TTS_MODEL}"
fi

# ── 4. Symlink volume models to /app/models ───────────────────────
# This ensures the app code always finds models at ./models/
if [ "${MODEL_DIR}" != "${APP_MODEL_DIR}" ]; then
    mkdir -p "$(dirname ${APP_MODEL_DIR})"
    if [ ! -L "${APP_MODEL_DIR}" ]; then
        ln -sf "${MODEL_DIR}" "${APP_MODEL_DIR}"
        echo "🔗 Symlinked ${MODEL_DIR} → ${APP_MODEL_DIR}"
    fi
fi

# ── 5. Create output directory ────────────────────────────────────
mkdir -p /app/output
mkdir -p "${VOLUME_DIR}/output" 2>/dev/null || true

# ── 6. Start the API ─────────────────────────────────────────────
echo ""
echo "🚀 Starting Voice Cloning API on port 8000..."
echo "═══════════════════════════════════════════"

exec python scripts/run_api.py