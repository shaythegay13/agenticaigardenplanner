#!/usr/bin/env python3
"""Test script to check Deepgram SDK imports and usage."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Try different import patterns
try:
    from deepgram import DeepgramClient, PrerecordedOptions, SpeakOptions
    print("✓ Successfully imported from deepgram")
except ImportError as e:
    print(f"✗ Cannot import from deepgram: {e}")
    
    # Try alternative imports
    try:
        from deepgram import DeepgramClient
        print("✓ Successfully imported DeepgramClient")
        
        # Check what's available
        client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
        print(f"✓ Client created")
        print(f"  Available methods: {dir(client)}")
        
        # Check listen methods
        print(f"\n  Listen methods: {dir(client.listen)}")
        
    except Exception as e2:
        print(f"✗ Error: {e2}")
