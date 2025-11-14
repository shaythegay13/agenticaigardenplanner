#!/bin/bash
# Start the Voice-Enabled Garden Planner API

echo "🌱 Starting Voice-Enabled Garden Planner API..."
echo ""
echo "Features:"
echo "  - Voice input (speech-to-text)"
echo "  - AI garden advice"
echo "  - Voice output (text-to-speech)"
echo "  - 270+ crops database"
echo "  - Climate-aware recommendations"
echo ""
echo "API will be available at: http://localhost:8001"
echo "Documentation at: http://localhost:8001/docs"
echo ""

# Activate virtual environment and run
cd "$(dirname "$0")"
./venv/bin/python voice_garden_api.py
