#!/usr/bin/env python3
"""
YouTube Transcript Summarizer

A command-line tool that:
1. Accepts a shortened YouTube URL as input
2. Downloads the video transcript from DownSub.com
3. Summarizes the transcript using OpenRouter API
4. Saves the summary as a Markdown file
"""

import os
import sys
import argparse
import logging
from config import logger, OPENROUTER_API_KEY

from utils.url_processor import process_youtube_url
from utils.transcript_downloader import TranscriptDownloader
from utils.summarizer import TranscriptSummarizer
from utils.markdown_generator import get_video_title, format_markdown, save_to_markdown

def main():
    """Main function to orchestrate the workflow."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Summarize YouTube video transcripts.')
    parser.add_argument('url', help='YouTube URL (e.g., https://youtu.be/dQw4w9WgXcQ)')
    parser.add_argument('--language', '-l', default='en', help='Preferred transcript language (default: en)')
    parser.add_argument('--output', '-o', help='Output file path (default: VIDEO_ID_summary.md)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Check if API key is set
    if not OPENROUTER_API_KEY:
        logger.error("OpenRouter API key is not set. Please set it in the .env file.")
        print("Error: OpenRouter API key is not set. Please set it in the .env file.")
        return 1
    
    # Process the YouTube URL
    logger.info(f"Processing URL: {args.url}")
    print(f"Processing YouTube URL: {args.url}")
    
    video_id, full_url = process_youtube_url(args.url)
    if not video_id or not full_url:
        logger.error(f"Invalid YouTube URL: {args.url}")
        print(f"Error: Invalid YouTube URL: {args.url}")
        return 1
    
    logger.info(f"Extracted video ID: {video_id}")
    print(f"Extracted video ID: {video_id}")
    
    # Download transcript
    logger.info("Downloading transcript...")
    print("Downloading transcript...")
    
    downloader = TranscriptDownloader()
    transcript = downloader.get_transcript(full_url, args.language)
    
    if not transcript:
        logger.error("Failed to download transcript")
        print("Error: Failed to download transcript. The video might not have subtitles or DownSub might be unavailable.")
        return 1
    
    logger.info(f"Successfully downloaded transcript ({len(transcript)} characters)")
    print(f"Successfully downloaded transcript ({len(transcript)} characters)")
    
    # Get video title
    video_title = get_video_title(full_url)
    if video_title:
        logger.info(f"Video title: {video_title}")
        print(f"Video title: {video_title}")
    else:
        logger.warning("Could not retrieve video title")
        print("Warning: Could not retrieve video title")
    
    # Summarize transcript
    logger.info("Summarizing transcript...")
    print("Summarizing transcript...")
    
    summarizer = TranscriptSummarizer()
    summary = summarizer.summarize_transcript(transcript)
    
    if not summary:
        logger.error("Failed to summarize transcript")
        print("Error: Failed to summarize transcript")
        return 1
    
    logger.info(f"Successfully generated summary ({len(summary)} characters)")
    print(f"Successfully generated summary ({len(summary)} characters)")
    
    # Format and save as Markdown
    logger.info("Generating Markdown...")
    print("Generating Markdown...")
    
    markdown_content = format_markdown(summary, args.url, video_id, video_title)
    
    # Use custom output path if provided
    output_path = args.output if args.output else None
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Saved summary to: {output_path}")
            print(f"Saved summary to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving to custom path: {str(e)}")
            print(f"Error saving to custom path: {str(e)}")
            output_path = None
    
    # If custom path failed or wasn't provided, use default
    if not output_path:
        saved_path = save_to_markdown(markdown_content, video_id)
        if saved_path:
            logger.info(f"Saved summary to: {saved_path}")
            print(f"Saved summary to: {saved_path}")
        else:
            logger.error("Failed to save summary")
            print("Error: Failed to save summary")
            return 1
    
    logger.info("Process completed successfully")
    print("Process completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
