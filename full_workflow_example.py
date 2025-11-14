#!/usr/bin/env python3
"""
Full workflow example: Audio input -> Transcription -> AI Response -> Audio output
"""

from garden_assistant import transcribe_audio, generate_response, synthesize_speech

def process_audio_question(audio_input_path):
    """
    Complete workflow for processing an audio question.
    
    Args:
        audio_input_path: Path to the user's audio file (WAV format)
    
    Returns:
        tuple: (transcript, ai_reply, output_audio_path)
    """
    print("=" * 60)
    print("Garden Assistant - Full Workflow")
    print("=" * 60)
    
    # Step 1: Transcribe the audio question
    print(f"\n[1/3] Transcribing audio from: {audio_input_path}")
    transcript = transcribe_audio(audio_input_path)
    
    if not transcript:
        print("❌ Failed to transcribe audio")
        return None, None, None
    
    print(f"✓ User asked: {transcript}")
    
    # Step 2: Generate AI response
    print(f"\n[2/3] Generating AI response...")
    ai_reply = generate_response(transcript)
    
    if not ai_reply:
        print("❌ Failed to generate AI response")
        return transcript, None, None
    
    print(f"✓ AI replies: {ai_reply}")
    
    # Step 3: Synthesize speech from AI response
    print(f"\n[3/3] Synthesizing speech...")
    output_audio = synthesize_speech(ai_reply, "ai_response.mp3")
    
    if not output_audio:
        print("❌ Failed to synthesize speech")
        return transcript, ai_reply, None
    
    print(f"✓ Audio saved to: {output_audio}")
    
    print("\n" + "=" * 60)
    print("✅ Workflow Complete!")
    print("=" * 60)
    
    return transcript, ai_reply, output_audio


if __name__ == "__main__":
    # Example usage
    audio_input_path = "user_input.wav"  # User records/uploaded question
    
    # Check if the file exists
    import os
    if not os.path.exists(audio_input_path):
        print(f"⚠️  Audio file '{audio_input_path}' not found.")
        print("\nTo test this workflow:")
        print("1. Record a garden-related question as 'user_input.wav'")
        print("2. Or use any WAV audio file and update the path above")
        print("\nFor now, here's what the workflow would look like:\n")
        
        # Demonstrate with sample data
        print("=" * 60)
        print("Garden Assistant - Full Workflow (Demo)")
        print("=" * 60)
        
        sample_transcript = "What vegetables should I plant in my garden during spring?"
        print(f"\n[1/3] Transcribing audio from: {audio_input_path}")
        print(f"✓ User asked: {sample_transcript}")
        
        print(f"\n[2/3] Generating AI response...")
        ai_reply = generate_response(sample_transcript)
        
        if ai_reply:
            print(f"✓ AI replies: {ai_reply}")
            
            print(f"\n[3/3] Synthesizing speech...")
            output_audio = synthesize_speech(ai_reply, "ai_response.mp3")
            
            if output_audio:
                print(f"✓ Audio saved to: {output_audio}")
                print("\n" + "=" * 60)
                print("✅ Workflow Complete!")
                print("=" * 60)
        else:
            print("⚠️  OpenAI quota exceeded. Using sample response instead.")
            sample_reply = """For spring planting, I recommend starting with cool-season vegetables like lettuce, 
spinach, peas, and radishes. These can tolerate light frosts and thrive in cooler temperatures. 
You can also start broccoli and cauliflower indoors about 6-8 weeks before your last frost date. 
Make sure to prepare your soil with compost and check your local frost dates before planting!"""
            
            print(f"✓ Sample AI reply: {sample_reply}")
            
            print(f"\n[3/3] Synthesizing speech...")
            output_audio = synthesize_speech(sample_reply, "ai_response.mp3")
            
            if output_audio:
                print(f"✓ Audio saved to: {output_audio}")
                print("\n" + "=" * 60)
                print("✅ Workflow Complete!")
                print("=" * 60)
    else:
        # Process the actual audio file
        transcript, ai_reply, output_audio = process_audio_question(audio_input_path)
        
        if transcript and ai_reply and output_audio:
            print(f"\nUser asked: {transcript}")
            print(f"AI replies: {ai_reply}")
            print(f"Audio output: {output_audio}")
            
            # Optional: Play the audio (requires additional library)
            print("\n💡 Tip: Play the audio with:")
            print(f"   - Linux: mpg123 {output_audio}")
            print(f"   - macOS: afplay {output_audio}")
            print(f"   - Windows: start {output_audio}")
