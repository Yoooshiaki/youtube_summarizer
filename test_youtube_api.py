#!/usr/bin/env python3
"""
Test script for youtube-transcript-api.
"""

import sys

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("Successfully imported youtube-transcript-api")
    
    # Try to get a transcript for a test video
    video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    print(f"Trying to get transcript for video ID: {video_id}")
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Successfully retrieved transcript with {len(transcript)} segments")
        print("First few segments:")
        for segment in transcript[:3]:
            print(segment)
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
    
except ImportError:
    print("Failed to import youtube-transcript-api. Make sure it's installed.")
    sys.exit(1)
