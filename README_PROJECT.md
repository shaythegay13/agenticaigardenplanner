# Voice-Enabled AI Garden Planner

A complete voice-first garden planning system combining Deepgram voice AI with a comprehensive 270+ crop database and climate-aware recommendations.

## 🎯 What This Does

Ask garden questions with your voice and get intelligent, spoken responses:

**You**: 🎤 *"What vegetables should I plant in spring?"*

**System**: 🔊 *"For spring planting, I recommend starting with cool-season vegetables like lettuce, spinach, peas, and radishes..."*

## ✨ Key Features

### Voice Capabilities
- 🎤 **Speech-to-Text**: Accurate transcription with Deepgram Nova-3
- 🔊 **Text-to-Speech**: Natural voice with Deepgram Aura
- 💬 **Natural Language**: Understands garden questions naturally
- 🌍 **Multi-format**: Supports WAV, MP3, and base64 audio

### Garden Intelligence
- 🌱 **270+ Crops**: Fruits, vegetables, herbs, nuts, grains
- 🌡️ **Climate-Aware**: Weather and hardiness zone recommendations
- 🦠 **Disease Database**: 300+ diseases with identification
- 🤝 **Companion Planting**: Strategic crop relationships
- 💧 **Water Management**: Cornell CSF-based irrigation
- 📅 **Seasonal Planning**: Year-round strategies
- 🗺️ **Regional Resources**: Location-specific guidance

## 🚀 Quick Start

### 1. Start the API
```bash
./start_voice_api.sh
```

### 2. Ask a Question
```bash
curl -X POST http://localhost:8001/api/voice/ask \
  -H "Content-Type: application/json" \
  -d '{"text_question": "What grows well in shade?"}'
```

### 3. View Documentation
Open http://localhost:8001/docs

## 📁 Project Files

```
windsurf-project/
├── 🎤 Voice Layer
│   ├── voice_garden_api.py          # Main API server
│   ├── garden_assistant.py          # Core functions
│   └── test_voice_api.py            # Test suite
│
├── 🌱 Backend
│   └── backend/                     # AI Garden Planner (270+ crops)
│
├── 📚 Documentation
│   ├── INTEGRATION_COMPLETE.md      # Full integration guide
│   ├── VOICE_API_GUIDE.md           # API documentation
│   └── SETUP_COMPLETE.md            # Setup instructions
│
└── 🔧 Configuration
    ├── .env.local                   # Your API keys
    └── requirements.txt             # Dependencies
```

## 🎯 Use Cases

### 1. Hands-Free Gardening
Ask questions while working in your garden with dirty hands.

### 2. Mobile Garden App
Voice-first mobile experience for on-the-go planning.

### 3. Accessibility
Complete voice interface for visually impaired users.

### 4. Smart Home Integration
"Hey Google, ask my garden planner what to plant this month."

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/voice/ask` | POST | Ask a question (voice or text) |
| `/api/voice/upload` | POST | Upload audio file |
| `/api/voice/speak` | POST | Convert text to speech |
| `/api/voice/garden-plan` | POST | Generate plan from voice |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive documentation |

## 💻 Code Examples

### Python
```python
from garden_assistant import transcribe_audio, generate_response, synthesize_speech

# Full workflow
transcript = transcribe_audio("question.wav")
answer = generate_response(transcript)
audio = synthesize_speech(answer)
```

### JavaScript
```javascript
const response = await fetch('/api/voice/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text_question: "When should I plant tomatoes?",
    location: "Boston, MA"
  })
});

const data = await response.json();
console.log(data.answer_text);
playAudio(data.audio_base64);
```

### cURL
```bash
curl -X POST http://localhost:8001/api/voice/ask \
  -H "Content-Type: application/json" \
  -d '{"text_question": "What grows in shade?"}'
```

## 🛠️ Tech Stack

- **Voice**: Deepgram (STT/TTS)
- **AI**: OpenAI GPT-3.5
- **API**: FastAPI
- **Backend**: Python 3.11
- **Database**: 270+ crops, 300+ diseases

## 📊 Performance

- **Transcription**: ~1-2 seconds
- **AI Response**: ~2-4 seconds  
- **Speech Synthesis**: ~1-2 seconds
- **Total**: ~4-8 seconds end-to-end

## 🔐 Security

- API keys stored in `.env.local` (gitignored)
- CORS configurable for production
- Rate limiting ready
- HTTPS recommended for production

## 📖 Documentation

- **Full Integration Guide**: `INTEGRATION_COMPLETE.md`
- **Voice API Guide**: `VOICE_API_GUIDE.md`
- **Setup Instructions**: `SETUP_COMPLETE.md`
- **Backend Docs**: `backend/README.md`

## 🧪 Testing

```bash
# Test voice API
./venv/bin/python test_voice_api.py

# Test full workflow
./venv/bin/python full_workflow_example.py

# Test text-to-speech
./venv/bin/python test_tts.py
```

## 🌟 Next Steps

1. **Build Frontend**: Create web/mobile UI
2. **Deploy**: Host on Heroku/AWS/GCP
3. **Extend**: Add more languages, features
4. **Integrate**: Connect with smart home systems

## 📝 License

MIT

## 🙏 Credits

- **Voice AI**: Deepgram
- **Language AI**: OpenAI
- **Garden Backend**: AI Garden Planner (270+ crops)
- **Framework**: FastAPI

---

**Ready to use!** Start the API and begin building your voice-enabled garden planning experience.

```bash
./start_voice_api.sh
```

Then visit http://localhost:8001/docs for interactive API documentation.
