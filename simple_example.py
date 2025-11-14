#!/usr/bin/env python3
"""
Simple example matching your exact workflow code.
"""

from garden_assistant import transcribe_audio, generate_response, synthesize_speech

# Your exact code:
audio_input_path = "user_input.wav"  # User records/uploaded question

transcript = transcribe_audio(audio_input_path)
ai_reply = generate_response(transcript)
output_audio = synthesize_speech(ai_reply)

print(f"User asked: {transcript}")
print(f"AI replies: {ai_reply}")
# Play output_audio on your machine with a media player module if desired
