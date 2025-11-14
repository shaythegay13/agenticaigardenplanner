#!/usr/bin/env python3
"""Test the text-to-speech functionality without using OpenAI."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

from deepgram import DeepgramClient

# Initialize Deepgram client
deepgram = DeepgramClient()

def test_text_to_speech():
    """Test Deepgram text-to-speech."""
    text = "Hello! I'm your garden planning assistant. I can help you with planting advice, seasonal tips, and garden care recommendations."
    output_path = "welcome_message.mp3"
    
    try:
        print(f"Generating speech for: '{text}'")
        response = deepgram.speak.v1.audio.generate(
            text=text,
            model="aura-asteria-en"
        )
        
        # The response is a generator, collect all chunks
        audio_data = b""
        for chunk in response:
            audio_data += chunk
        
        # Save the audio file
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_data)
        
        print(f"✓ Success! Audio saved to: {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        return output_path
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_text_to_speech()
