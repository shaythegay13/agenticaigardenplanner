#!/usr/bin/env python3
"""
Create a sample audio file to test the full workflow.
This uses Deepgram TTS to create a sample question audio file.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

from deepgram import DeepgramClient

def create_sample_question(text, output_path="user_input.wav"):
    """Create a sample audio question using Deepgram TTS."""
    print(f"Creating sample audio question: '{text}'")
    
    deepgram = DeepgramClient()
    
    try:
        response = deepgram.speak.v1.audio.generate(
            text=text,
            model="aura-asteria-en"
        )
        
        # Collect audio data
        audio_data = b""
        for chunk in response:
            audio_data += chunk
        
        # Save as MP3 first (Deepgram outputs MP3)
        temp_mp3 = output_path.replace('.wav', '.mp3')
        with open(temp_mp3, "wb") as audio_file:
            audio_file.write(audio_data)
        
        print(f"✓ Sample audio created: {temp_mp3}")
        print(f"  File size: {len(audio_data)} bytes")
        print(f"\n💡 Note: Deepgram outputs MP3 format.")
        print(f"   You can use '{temp_mp3}' directly with transcribe_audio()")
        print(f"   Or convert to WAV using: ffmpeg -i {temp_mp3} {output_path}")
        
        return temp_mp3
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


if __name__ == "__main__":
    # Create a sample garden question
    sample_questions = [
        "What vegetables should I plant in my garden during spring?",
        "How often should I water my tomato plants?",
        "What's the best way to prepare soil for a vegetable garden?",
        "When is the best time to plant carrots?",
    ]
    
    print("=" * 60)
    print("Sample Audio Creator")
    print("=" * 60)
    print("\nAvailable sample questions:")
    for i, q in enumerate(sample_questions, 1):
        print(f"{i}. {q}")
    
    print(f"\nCreating audio for question 1...\n")
    
    audio_file = create_sample_question(
        sample_questions[0],
        "user_input.wav"
    )
    
    if audio_file:
        print(f"\n✅ Ready to test! Run:")
        print(f"   ./venv/bin/python full_workflow_example.py")
        print(f"\nOr update the path in your script to use: {audio_file}")
