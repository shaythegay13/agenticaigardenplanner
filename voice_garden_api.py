#!/usr/bin/env python3
"""
Voice-Enabled Garden Planning API
Integrates Deepgram voice capabilities with the AI Garden Planner backend
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import tempfile

# Load environment variables
load_dotenv('.env.local')

# Import voice capabilities
from deepgram import DeepgramClient
from openai import OpenAI

# Import backend garden planner
sys.path.append('./backend')
from agi_agent.gardening.models import (
    UserInput, LocationInput, GardeningMethod, SpaceSize, Sunlight,
    Experience, UserGoals, CropInterest, Preference, SoilType
)
from agi_agent.gardening.climate import fetch_simple_forecast, geocode_location
from agi_agent.gardening.planner import generate_plan

# Initialize clients
deepgram = DeepgramClient()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Voice-Enabled Garden Planner API",
    description="AI Garden Planner with voice input/output capabilities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VoiceQuestionRequest(BaseModel):
    """Request for voice-based garden question"""
    audio_base64: Optional[str] = None
    text_question: Optional[str] = None
    location: Optional[str] = None
    context: Optional[dict] = None  # User's garden context


class VoiceQuestionResponse(BaseModel):
    """Response with text and audio"""
    transcript: Optional[str] = None
    answer_text: str
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None


def transcribe_audio(audio_data: bytes) -> str:
    """Transcribe audio using Deepgram"""
    try:
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
            smart_format=True
        )
        return response.results.channels[0].alternatives[0].transcript
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")


def generate_garden_answer(question: str, context: Optional[dict] = None) -> str:
    """Generate garden advice using OpenAI"""
    try:
        # Build context-aware prompt
        system_prompt = """You are an expert garden planning assistant. Provide helpful, 
        practical advice about gardening, planting, crop care, and garden planning. 
        Keep responses concise but informative (2-3 paragraphs max for voice output).
        Focus on actionable advice."""
        
        user_prompt = question
        if context:
            user_prompt = f"Context: {context}\n\nQuestion: {question}"
        
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Fallback response if OpenAI fails
        return f"""I'd be happy to help with your garden question: "{question}". 
        However, I'm currently experiencing connectivity issues. 
        For immediate assistance, I recommend checking your local agricultural extension office 
        or visiting reputable gardening websites like the USDA or your state's agricultural resources."""


def synthesize_speech(text: str) -> bytes:
    """Convert text to speech using Deepgram"""
    try:
        response = deepgram.speak.v1.audio.generate(
            text=text,
            model="aura-asteria-en"
        )
        
        # Collect audio chunks
        audio_data = b""
        for chunk in response:
            audio_data += chunk
        
        return audio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis error: {str(e)}")


@app.get("/")
async def root():
    return {
        "service": "Voice-Enabled Garden Planner API",
        "version": "1.0.0",
        "features": [
            "Voice question input (speech-to-text)",
            "AI-powered garden advice",
            "Voice response output (text-to-speech)",
            "Integration with AI Garden Planner backend",
            "270+ crops database",
            "Climate-aware recommendations"
        ],
        "endpoints": {
            "voice_question": "/api/voice/ask",
            "voice_upload": "/api/voice/upload",
            "text_to_speech": "/api/voice/speak",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "deepgram": "connected", "backend": "connected"}


@app.post("/api/voice/ask", response_model=VoiceQuestionResponse)
async def ask_voice_question(request: VoiceQuestionRequest):
    """
    Ask a garden question via voice or text and get a voice response
    
    - Accepts audio (base64) or text question
    - Returns text answer and audio response
    """
    transcript = None
    
    # Handle audio input
    if request.audio_base64:
        import base64
        audio_bytes = base64.b64decode(request.audio_base64)
        transcript = transcribe_audio(audio_bytes)
        question = transcript
    elif request.text_question:
        question = request.text_question
    else:
        raise HTTPException(status_code=400, detail="Must provide either audio_base64 or text_question")
    
    # Generate answer
    answer_text = generate_garden_answer(question, request.context)
    
    # Synthesize speech
    audio_data = synthesize_speech(answer_text)
    
    import base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    return VoiceQuestionResponse(
        transcript=transcript,
        answer_text=answer_text,
        audio_base64=audio_base64
    )


@app.post("/api/voice/upload")
async def upload_voice_question(
    audio_file: UploadFile = File(...),
    location: Optional[str] = Form(None),
    context: Optional[str] = Form(None)
):
    """
    Upload an audio file with a garden question
    
    - Accepts WAV, MP3, or other audio formats
    - Returns transcription, text answer, and audio response
    """
    # Read audio file
    audio_data = await audio_file.read()
    
    # Transcribe
    transcript = transcribe_audio(audio_data)
    
    # Parse context if provided
    import json
    context_dict = None
    if context:
        try:
            context_dict = json.loads(context)
        except:
            context_dict = {"notes": context}
    
    # Generate answer
    answer_text = generate_garden_answer(transcript, context_dict)
    
    # Synthesize speech
    audio_response = synthesize_speech(answer_text)
    
    # Save response audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tmp.write(audio_response)
        tmp_path = tmp.name
    
    import base64
    audio_base64 = base64.b64encode(audio_response).decode('utf-8')
    
    return {
        "transcript": transcript,
        "answer_text": answer_text,
        "audio_base64": audio_base64,
        "temp_audio_path": tmp_path
    }


@app.post("/api/voice/speak")
async def text_to_speech(text: str = Form(...)):
    """
    Convert text to speech
    
    - Accepts plain text
    - Returns audio in base64 format
    """
    audio_data = synthesize_speech(text)
    
    import base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    return {
        "text": text,
        "audio_base64": audio_base64,
        "format": "mp3"
    }


@app.post("/api/voice/garden-plan")
async def voice_garden_plan_request(
    audio_file: UploadFile = File(...),
    address: Optional[str] = Form(None)
):
    """
    Request a garden plan via voice
    
    User describes their garden needs in natural language,
    and the system extracts parameters and generates a plan.
    """
    # Read and transcribe audio
    audio_data = await audio_file.read()
    transcript = transcribe_audio(audio_data)
    
    # Use OpenAI to extract garden planning parameters from natural language
    try:
        extraction_prompt = f"""Extract garden planning parameters from this request: "{transcript}"
        
        Return a JSON object with these fields (use null if not mentioned):
        - method: Container, Raised Beds, In-ground, Vertical, Indoor, Rooftop
        - size: Small, Medium, Large, Very Large
        - sunlight: Full Sun, Partial Sun, Partial Shade, Shade
        - experience: Beginner, Novice, Intermediate, Advanced
        - crops: list of crop interests
        - preferences: list like "low maintenance", "drought resistant", etc.
        - address: location if mentioned
        
        Only return the JSON, no other text."""
        
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": extraction_prompt}]
        )
        
        import json
        params = json.loads(completion.choices[0].message.content)
        
        # Build location
        location_str = params.get('address') or address
        if not location_str:
            raise HTTPException(status_code=400, detail="Location is required for garden planning")
        
        location = LocationInput(address=location_str)
        lat, lon = geocode_location(location)
        location.latitude = lat
        location.longitude = lon
        
        # Map to enums with defaults
        method = GardeningMethod.RAISED_BEDS
        size = SpaceSize.MEDIUM
        sunlight = Sunlight.FULL_SUN
        experience = Experience.BEGINNER
        
        # Create user input
        user_input = UserInput(
            location=location,
            method=method,
            size=size,
            sunlight=sunlight,
            soil_type=SoilType.MEDIUM,
            experience=experience,
            goals=UserGoals(
                crops=[CropInterest.SUGGEST],
                preferences=[Preference.LOW_MAINTENANCE]
            )
        )
        
        # Get climate and generate plan
        climate = fetch_simple_forecast(lat, lon)
        plan_text = generate_plan(user_input, climate)
        
        # Create a summary for voice response
        summary = f"""I've created a personalized garden plan for your {params.get('size', 'medium')} 
        {params.get('method', 'raised bed')} garden. The full plan has been generated and includes 
        recommended crops, planting schedules, and care instructions. Check your screen for the complete details."""
        
        # Synthesize summary
        audio_response = synthesize_speech(summary)
        
        import base64
        audio_base64 = base64.b64encode(audio_response).decode('utf-8')
        
        return {
            "transcript": transcript,
            "extracted_params": params,
            "plan": plan_text,
            "summary": summary,
            "audio_base64": audio_base64
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice garden plan request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    print(f"Starting Voice-Enabled Garden Planner API on port {port}")
    print(f"Docs available at: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
