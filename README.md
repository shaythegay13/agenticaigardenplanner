# Garden Assistant

A voice-enabled garden planning assistant using Deepgram for speech-to-text/text-to-speech and OpenAI for intelligent responses.

## Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   ./venv/bin/pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env.local` file in the project root
   - Add your API keys:
     ```
     DEEPGRAM_API_KEY=YOUR_DEEPGRAM_API_KEY
     OPENAI_API_KEY=YOUR_OPENAI_API_KEY
     ```
   - Get API keys from:
     - `DEEPGRAM_API_KEY`: [Deepgram Console](https://console.deepgram.com/)
     - `OPENAI_API_KEY`: [OpenAI Platform](https://platform.openai.com/api-keys)

4. **Run the script:**
   ```bash
   ./venv/bin/python garden_assistant.py
   ```

## Features

- **Speech-to-Text**: Transcribe audio questions about gardening
- **AI Garden Advice**: Get intelligent responses from OpenAI
- **Text-to-Speech**: Convert advice to audio output

## Usage

### Direct Text Input
```python
from garden_assistant import generate_response, synthesize_speech

advice = generate_response("What vegetables should I plant in spring?")
audio_file = synthesize_speech(advice)
```

### Audio Input
```python
from garden_assistant import transcribe_audio, generate_response, synthesize_speech

transcript = transcribe_audio("question.wav")
advice = generate_response(transcript)
audio_file = synthesize_speech(advice)
```

## Current Status

✅ **Working:**
- Deepgram Speech-to-Text (transcription)
- Deepgram Text-to-Speech (synthesis)
- Environment variable loading
- Virtual environment setup

⚠️ **Note:** OpenAI integration requires active API credits. The demo runs with sample text if OpenAI quota is exceeded.

## Security Note

**IMPORTANT**: Never commit your `.env.local` file with actual API keys to version control. The file is already in `.gitignore` to prevent accidental commits. If you accidentally expose API keys:
1. Revoke the exposed keys immediately from your provider dashboards
2. Generate new keys
3. Update your `.env.local` file with the new keys
