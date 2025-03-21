#!/usr/bin/env python3
"""
Test script for the YouTube Transcript Summarizer.

This script tests the functionality of the summarizer with a sample YouTube URL.
"""

import os
import sys
import logging

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import setup_logging
from utils.url_processor import process_youtube_url
from utils.transcript_downloader import TranscriptDownloader
from utils.summarizer import TranscriptSummarizer
from utils.markdown_generator import get_video_title, format_markdown, save_to_markdown

# Set up logging
logger = setup_logging()
logger.setLevel(logging.INFO)

def test_url_processor():
    """Test the URL processor."""
    print("\n=== Testing URL Processor ===")
    
    # Test with a valid shortened URL
    url = "https://youtu.be/dQw4w9WgXcQ"
    video_id, full_url = process_youtube_url(url)
    
    print(f"URL: {url}")
    print(f"Video ID: {video_id}")
    print(f"Full URL: {full_url}")
    
    assert video_id == "dQw4w9WgXcQ", "Failed to extract correct video ID"
    assert full_url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Failed to generate correct full URL"
    
    print("URL Processor test passed!")

def test_transcript_downloader(url):
    """Test the transcript downloader."""
    print("\n=== Testing Transcript Downloader ===")
    
    video_id, full_url = process_youtube_url(url)
    if not video_id or not full_url:
        print(f"Invalid URL: {url}")
        return False
    
    print(f"Downloading transcript for: {full_url}")
    
    downloader = TranscriptDownloader()
    transcript = downloader.get_transcript(full_url)
    
    if not transcript:
        print("Failed to download transcript")
        return False
    
    print(f"Successfully downloaded transcript ({len(transcript)} characters)")
    print(f"Transcript preview: {transcript[:150]}...")
    
    return transcript

def test_summarizer(transcript):
    """Test the summarizer."""
    print("\n=== Testing Summarizer ===")
    
    if not transcript:
        print("No transcript to summarize")
        return False
    
    print("Summarizing transcript...")
    
    summarizer = TranscriptSummarizer()
    summary = summarizer.summarize_transcript(transcript)
    
    if not summary:
        print("Failed to summarize transcript")
        return False
    
    print(f"Successfully generated summary ({len(summary)} characters)")
    print(f"Summary preview: {summary[:150]}...")
    
    return summary

def test_markdown_generator(summary, url):
    """Test the markdown generator."""
    print("\n=== Testing Markdown Generator ===")
    
    if not summary:
        print("No summary to format")
        return False
    
    video_id, full_url = process_youtube_url(url)
    if not video_id or not full_url:
        print(f"Invalid URL: {url}")
        return False
    
    # Get video title
    print(f"Getting title for: {full_url}")
    video_title = get_video_title(full_url)
    
    if video_title:
        print(f"Video title: {video_title}")
    else:
        print("Could not retrieve video title")
    
    # Format markdown
    print("Formatting markdown...")
    markdown_content = format_markdown(summary, url, video_id, video_title)
    
    # Save to file
    print("Saving to file...")
    test_filename = f"test_{video_id}_summary.md"
    
    try:
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Saved test summary to: {test_filename}")
        return True
    except Exception as e:
        print(f"Error saving test file: {str(e)}")
        return False

def main():
    """Main test function."""
    print("=== YouTube Transcript Summarizer Test ===")
    
    # Test URL (Rick Astley - Never Gonna Give You Up)
    test_url = "https://youtu.be/dQw4w9WgXcQ"
    
    # Test URL processor
    test_url_processor()
    
    # Test transcript downloader
    transcript = test_transcript_downloader(test_url)
    
    if transcript:
        # Test summarizer
        summary = test_summarizer(transcript)
        
        if summary:
            # Test markdown generator
            success = test_markdown_generator(summary, test_url)
            
            if success:
                print("\n=== All tests completed successfully! ===")
                return 0
    
    print("\n=== Some tests failed ===")
    return 1

if __name__ == "__main__":
    sys.exit(main())
