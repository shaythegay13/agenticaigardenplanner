# Install modules
# pip install deepgram-sdk openai flask

import os
from dotenv import load_dotenv

# Load environment variables from .env.local FIRST
load_dotenv('.env.local')

# Load API keys from environment variables
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")  # Deepgram API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI key

# Validate API keys
if not DG_API_KEY:
    raise ValueError("DEEPGRAM_API_KEY not found in environment. Please check your .env.local file.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment. Please check your .env.local file.")

# Now import and initialize clients (after env vars are set)
from deepgram import DeepgramClient
from openai import OpenAI

deepgram = DeepgramClient()  # Reads DEEPGRAM_API_KEY from environment
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe_audio(audio_path):
    """Transcribe audio file using Deepgram."""
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
            smart_format=True
        )
        return response.results.channels[0].alternatives[0].transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def generate_response(text):
    """Generate garden advice using OpenAI."""
    try:
        prompt = f"You are a garden planning assistant. Reply with garden advice for: {text}."
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def synthesize_speech(text, output_path="output.mp3"):
    """Synthesize speech using Deepgram."""
    try:
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
        
        return output_path
    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example: Process audio input
    # transcript = transcribe_audio("input.wav")
    # if transcript:
    #     print(f"Transcript: {transcript}")
    #     advice = generate_response(transcript)
    #     if advice:
    #         print(f"Advice: {advice}")
    #         audio_file = synthesize_speech(advice)
    #         print(f"Audio saved to: {audio_file}")
    
    # Example: Direct text input (without OpenAI due to quota)
    print("=" * 60)
    print("Garden Assistant - Text-to-Speech Demo")
    print("=" * 60)
    
    # Since OpenAI has quota issues, let's just test TTS with a sample response
    sample_advice = """For spring planting, consider these vegetables:
    
1. Lettuce and leafy greens - They thrive in cooler spring temperatures
2. Peas - Plant as soon as soil can be worked
3. Radishes - Quick-growing and cold-tolerant
4. Carrots - Can handle light frosts
5. Broccoli - Start indoors 6-8 weeks before last frost

Remember to check your local frost dates and prepare your soil with compost!"""
    
    print(f"\nSample Garden Advice:\n{sample_advice}\n")
    
    audio_file = synthesize_speech(sample_advice, "garden_advice.mp3")
    if audio_file:
        print(f"✓ Audio response saved to: {audio_file}")
    
    # Uncomment below when you have OpenAI credits:
    # user_question = "What vegetables should I plant in spring?"
    # advice = generate_response(user_question)
    # if advice:
    #     print(f"Garden Advice: {advice}")
    #     audio_file = synthesize_speech(advice)
    #     if audio_file:
    #         print(f"Audio response saved to: {audio_file}")
