# Voice-Enabled Garden Planner API Guide

## Overview

This integration combines your comprehensive AI Garden Planner backend with Deepgram voice capabilities, creating a voice-first garden planning experience.

## Architecture

```
┌─────────────────┐
│  Voice Input    │ (User speaks question)
│  (Deepgram STT) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Processing  │ (OpenAI + Garden Backend)
│  - Question     │
│  - Context      │
│  - Garden DB    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Voice Output   │ (Deepgram TTS)
│  + Text         │
└─────────────────┘
```

## API Endpoints

### 1. Voice Question (`POST /api/voice/ask`)

Ask a garden question via voice or text.

**Request:**
```json
{
  "audio_base64": "base64_encoded_audio",  // Optional
  "text_question": "What should I plant?",  // Optional
  "location": "New York, NY",               // Optional
  "context": {                              // Optional
    "garden_size": "medium",
    "experience": "beginner"
  }
}
```

**Response:**
```json
{
  "transcript": "What vegetables should I plant in spring?",
  "answer_text": "For spring planting in your area...",
  "audio_base64": "base64_encoded_response_audio"
}
```

### 2. Upload Audio (`POST /api/voice/upload`)

Upload an audio file with a question.

**Request:** (multipart/form-data)
- `audio_file`: Audio file (WAV, MP3, etc.)
- `location`: Optional location string
- `context`: Optional JSON context

**Response:**
```json
{
  "transcript": "transcribed question",
  "answer_text": "detailed answer",
  "audio_base64": "response audio",
  "temp_audio_path": "/tmp/response.mp3"
}
```

### 3. Text-to-Speech (`POST /api/voice/speak`)

Convert any text to speech.

**Request:** (form data)
- `text`: Text to convert

**Response:**
```json
{
  "text": "original text",
  "audio_base64": "audio data",
  "format": "mp3"
}
```

### 4. Voice Garden Plan (`POST /api/voice/garden-plan`)

Request a full garden plan via natural language voice input.

**Request:** (multipart/form-data)
- `audio_file`: User describing their garden needs
- `address`: Optional location

**Response:**
```json
{
  "transcript": "I want a medium raised bed garden...",
  "extracted_params": {
    "method": "Raised Beds",
    "size": "Medium",
    "crops": ["tomatoes", "lettuce"]
  },
  "plan": "Full garden plan text...",
  "summary": "Voice-friendly summary",
  "audio_base64": "summary audio"
}
```

## Integration with Backend

The voice API seamlessly integrates with your existing backend:

### Backend Features Available:
- ✅ 270+ crops database
- ✅ Climate-aware recommendations
- ✅ Disease identification
- ✅ Companion planting
- ✅ Water management
- ✅ Seasonal planning
- ✅ Regional resources

### Voice Layer Adds:
- 🎤 Speech-to-text (Deepgram Nova-3)
- 🔊 Text-to-speech (Deepgram Aura)
- 💬 Natural language processing (OpenAI)
- 🎯 Context-aware responses

## Running the API

### Start the Voice API:
```bash
./venv/bin/python voice_garden_api.py
```

The API runs on port 8001 by default.

### Test the API:
```bash
./venv/bin/python test_voice_api.py
```

### Access Documentation:
Open http://localhost:8001/docs for interactive API documentation.

## Example Usage

### Python Client:
```python
import requests
import base64

# Ask a text question
response = requests.post(
    "http://localhost:8001/api/voice/ask",
    json={
        "text_question": "What vegetables grow well in shade?",
        "location": "Seattle, WA"
    }
)

data = response.json()
print(data['answer_text'])

# Save audio response
audio_bytes = base64.b64decode(data['audio_base64'])
with open('response.mp3', 'wb') as f:
    f.write(audio_bytes)
```

### JavaScript/Frontend:
```javascript
// Ask question with audio
const formData = new FormData();
formData.append('audio_file', audioBlob);
formData.append('location', 'Boston, MA');

const response = await fetch('http://localhost:8001/api/voice/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.answer_text);

// Play audio response
const audioData = atob(data.audio_base64);
const audioBlob = new Blob([audioData], { type: 'audio/mp3' });
const audioUrl = URL.createObjectURL(audioBlob);
const audio = new Audio(audioUrl);
audio.play();
```

## Use Cases

### 1. Voice Garden Assistant
Users can ask questions while working in their garden:
- "When should I water my tomatoes?"
- "What's wrong with my cucumber leaves?"
- "Can I plant basil next to tomatoes?"

### 2. Hands-Free Planning
Create garden plans through conversation:
- "I want to start a small container garden on my balcony"
- "Help me plan a vegetable garden for beginners"

### 3. Accessibility
Voice interface makes garden planning accessible to:
- Users with visual impairments
- Users with mobility limitations
- Users who prefer voice interaction

### 4. Mobile Experience
Perfect for mobile apps where typing is inconvenient.

## Environment Variables

Required in `.env.local`:
```
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
```

## Dependencies

The voice API uses your existing backend dependencies plus:
- `deepgram-sdk` - Voice capabilities
- `openai` - Natural language processing
- `fastapi` - API framework
- `uvicorn` - ASGI server

All already installed in your virtual environment!

## Next Steps

1. **Start the API**: `./venv/bin/python voice_garden_api.py`
2. **Test it**: `./venv/bin/python test_voice_api.py`
3. **Build a frontend**: Use the API endpoints in your web/mobile app
4. **Deploy**: Deploy alongside your existing backend

## Notes

- The API handles OpenAI quota issues gracefully with fallback responses
- Audio format is MP3 (compatible with all browsers)
- Supports both base64 and file upload for audio
- CORS enabled for frontend integration
- Full FastAPI documentation at `/docs` endpoint
