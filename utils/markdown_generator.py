import os
import re
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def get_video_title(video_url):
    """
    Get the title of the YouTube video.
    
    Args:
        video_url (str): The YouTube URL
        
    Returns:
        str: Video title or None if not found
    """
    try:
        logger.info(f"Fetching video title for: {video_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different methods to find the title
        # Method 1: Look for the title tag
        title = soup.find('title')
        if title:
            # Clean up the title (remove " - YouTube" suffix)
            title_text = title.text.strip()
            title_text = re.sub(r'\s*-\s*YouTube$', '', title_text)
            logger.info(f"Found video title: {title_text}")
            return title_text
        
        # Method 2: Look for meta tags
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            logger.info(f"Found video title from meta tag: {meta_title['content']}")
            return meta_title['content']
        
        logger.warning("Could not find video title")
        return None
    
    except Exception as e:
        logger.error(f"Error fetching video title: {str(e)}")
        return None

def format_markdown(summary, video_url, video_id, video_title=None):
    """
    Format the summary as Markdown.
    
    Args:
        summary (str): The summary text
        video_url (str): The YouTube URL
        video_id (str): The YouTube video ID
        video_title (str, optional): The video title. Defaults to None.
        
    Returns:
        str: Formatted Markdown content
    """
    logger.info("Formatting summary as Markdown")
    
    # Use video ID as title if no title is provided
    if not video_title:
        video_title = f"YouTube Video {video_id}"
    
    # Get current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Format the Markdown
    markdown = f"""# Video Summary: {video_title}

## Summary

{summary}

## Metadata
- Original URL: {video_url}
- Video ID: {video_id}
- Processed on: {current_date}
"""
    
    logger.info(f"Created Markdown content ({len(markdown)} characters)")
    return markdown

def save_to_markdown(markdown_content, video_id):
    """
    Save Markdown content to a file.
    
    Args:
        markdown_content (str): The Markdown content
        video_id (str): The YouTube video ID
        
    Returns:
        str: Path to the saved file or None if failed
    """
    if not markdown_content or not video_id:
        logger.error("Cannot save: Missing content or video ID")
        return None
    
    try:
        # Create filename
        filename = f"{video_id}_summary.md"
        
        logger.info(f"Saving Markdown to file: {filename}")
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Get absolute path
        abs_path = os.path.abspath(filename)
        logger.info(f"Successfully saved Markdown to: {abs_path}")
        
        return abs_path
    
    except Exception as e:
        logger.error(f"Error saving Markdown file: {str(e)}")
        return None
