import re
import logging
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

def validate_youtube_url(url):
    """
    Validate if the URL is a valid YouTube URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    # Check for shortened youtu.be format
    youtu_be_pattern = r'^https?://youtu\.be/[a-zA-Z0-9_-]{11}$'
    # Check for standard youtube.com format
    youtube_com_pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}(?:&\S*)?$'
    
    if re.match(youtu_be_pattern, url) or re.match(youtube_com_pattern, url):
        logger.info(f"Valid YouTube URL: {url}")
        return True
    
    logger.warning(f"Invalid YouTube URL: {url}")
    return False

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url (str): The YouTube URL
        
    Returns:
        str: The video ID or None if not found
    """
    try:
        # Handle youtu.be format
        if 'youtu.be' in url:
            path = urlparse(url).path
            video_id = path.strip('/')
            logger.info(f"Extracted video ID from youtu.be URL: {video_id}")
            return video_id
        
        # Handle youtube.com format
        elif 'youtube.com' in url:
            query = urlparse(url).query
            params = parse_qs(query)
            video_id = params.get('v', [None])[0]
            logger.info(f"Extracted video ID from youtube.com URL: {video_id}")
            return video_id
        
        else:
            logger.error(f"Unsupported URL format: {url}")
            return None
    
    except Exception as e:
        logger.error(f"Error extracting video ID from {url}: {str(e)}")
        return None

def get_full_youtube_url(video_id):
    """
    Convert video ID to full YouTube URL.
    
    Args:
        video_id (str): The YouTube video ID
        
    Returns:
        str: The full YouTube URL
    """
    if not video_id:
        logger.error("Cannot create YouTube URL: video ID is None")
        return None
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    logger.info(f"Created full YouTube URL: {url}")
    return url

def process_youtube_url(url):
    """
    Process a YouTube URL: validate, extract ID, and convert to full URL if needed.
    
    Args:
        url (str): The YouTube URL to process
        
    Returns:
        tuple: (video_id, full_url) or (None, None) if invalid
    """
    if not validate_youtube_url(url):
        return None, None
    
    video_id = extract_video_id(url)
    if not video_id:
        return None, None
    
    full_url = get_full_youtube_url(video_id)
    return video_id, full_url
