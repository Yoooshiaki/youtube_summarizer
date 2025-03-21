import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class TranscriptDownloader:
    """Class to handle downloading transcripts using youtube-transcript-api"""
    
    def __init__(self):
        pass
    
    def get_transcript(self, youtube_url, language="en"):
        """
        Main function to get transcript from YouTube.
        
        Args:
            youtube_url (str): The YouTube URL
            language (str): Preferred language code (default: "en" for English)
            
        Returns:
            str: Transcript content or None if failed
        """
        logger.info(f"Getting transcript for YouTube URL: {youtube_url}")
        
        # Extract video ID from URL
        video_id = self._extract_video_id(youtube_url)
        if not video_id:
            logger.error(f"Could not extract video ID from URL: {youtube_url}")
            return None
        
        try:
            # Get transcript using YouTubeTranscriptApi
            logger.info(f"Fetching transcript for video ID: {video_id}")
            
            try:
                # First try to get the transcript directly
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
                logger.info(f"Found transcript in language: {language}")
            except NoTranscriptFound:
                # If the specified language is not available, try to get any available transcript
                logger.warning(f"No transcript found for language '{language}', trying to get any available transcript")
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    available_transcript = transcript_list.find_transcript([])
                    transcript_data = available_transcript.fetch()
                    logger.info(f"Found transcript in language: {available_transcript.language_code}")
                except Exception as e:
                    logger.error(f"Error finding alternative transcript: {str(e)}")
                    return None
            
            # Convert transcript data to plain text
            text_content = self._convert_transcript_to_text(transcript_data)
            
            logger.info(f"Successfully downloaded transcript ({len(text_content)} characters)")
            return text_content
            
        except TranscriptsDisabled:
            logger.error(f"Transcripts are disabled for video: {video_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting transcript for video {video_id}: {str(e)}")
            return None
    
    def _extract_video_id(self, youtube_url):
        """
        Extract video ID from YouTube URL.
        
        Args:
            youtube_url (str): The YouTube URL
            
        Returns:
            str: The video ID or None if not found
        """
        try:
            # Handle youtu.be format
            if 'youtu.be' in youtube_url:
                path = urlparse(youtube_url).path
                video_id = path.strip('/').split('?')[0]
                logger.info(f"Extracted video ID from youtu.be URL: {video_id}")
                return video_id
            
            # Handle youtube.com format
            elif 'youtube.com' in youtube_url:
                query = urlparse(youtube_url).query
                params = parse_qs(query)
                video_id = params.get('v', [None])[0]
                logger.info(f"Extracted video ID from youtube.com URL: {video_id}")
                return video_id
            
            else:
                logger.error(f"Unsupported URL format: {youtube_url}")
                return None
        
        except Exception as e:
            logger.error(f"Error extracting video ID from {youtube_url}: {str(e)}")
            return None
    
    def _convert_transcript_to_text(self, transcript_data):
        """
        Convert transcript data to plain text.
        
        Args:
            transcript_data (list): List of transcript segments
            
        Returns:
            str: Plain text content
        """
        logger.info("Converting transcript data to plain text")
        
        # Each segment has 'text', 'start', and 'duration' keys
        text_parts = []
        for segment in transcript_data:
            if 'text' in segment and segment['text'].strip():
                text_parts.append(segment['text'].strip())
        
        return ' '.join(text_parts)
