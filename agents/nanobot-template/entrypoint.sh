#!/bin/sh
set -e

if [ -z "$GROQ_API_KEY" ]; then
  echo "ERROR: GROQ_API_KEY not set" >&2
  exit 1
fi

if [ -z "$DISCORD_TOKEN" ]; then
  echo "ERROR: DISCORD_TOKEN not set" >&2
  exit 1
fi

# DISCORD_USER_ID defaults to * (allow all) if not set
DISCORD_USER_ID="${DISCORD_USER_ID:-*}"

sed \
  -e "s|__GROQ_API_KEY__|$GROQ_API_KEY|g" \
  -e "s|__DISCORD_TOKEN__|$DISCORD_TOKEN|g" \
  -e "s|__DISCORD_USER_ID__|$DISCORD_USER_ID|g" \
  /app/config/config.template.json > /app/config/config.json

echo "Config generated. Starting nanobot gateway..."

exec nanobot gateway \
  --config /app/config/config.json \
  --workspace /app/workspace
