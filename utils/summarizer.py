import logging
import json
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class TranscriptSummarizer:
    """Class to handle summarizing transcripts using OpenRouter API"""
    
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(self, api_key=None, model=None):
        """
        Initialize the summarizer with API key and model.
        
        Args:
            api_key (str, optional): OpenRouter API key. Defaults to config value.
            model (str, optional): Model to use. Defaults to config value.
        """
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or OPENROUTER_MODEL
        
        if not self.api_key:
            logger.warning("No OpenRouter API key provided. Summarization will not work.")
    
    def create_summary_prompt(self, transcript, max_length=4000):
        """
        Create a prompt for the LLM to summarize the transcript.
        
        Args:
            transcript (str): The transcript text
            max_length (int, optional): Maximum length of transcript to include. Defaults to 4000.
            
        Returns:
            list: List of message objects for the API
        """
        # Truncate transcript if it's too long
        if len(transcript) > max_length:
            logger.info(f"Truncating transcript from {len(transcript)} to {max_length} characters")
            transcript = transcript[:max_length] + "..."
        
        # Create the messages for the API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes video transcripts. Create a concise summary in Japanese that captures the main points and key information from the transcript. The summary should be well-structured and informative."
            },
            {
                "role": "user",
                #"content": f"Please summarize the following video transcript in 3-5 paragraphs:\n\n{transcript}"
                "content": f"この動画スクリプトをわかりやすく、網羅的に要約してください paragraphs:\n\n{transcript}"
            }
        ]
        
        return messages
    
    def summarize_with_llm(self, messages):
        """
        Send prompt to LLM and get summary.
        
        Args:
            messages (list): List of message objects for the API
            
        Returns:
            str: Summary text or None if failed
        """
        if not self.api_key:
            logger.error("Cannot summarize: No API key provided")
            return None
        
        try:
            logger.info(f"Sending request to OpenRouter API using model: {self.model}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages
            }
            
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the summary from the response
            if 'choices' in result and len(result['choices']) > 0:
                summary = result['choices'][0]['message']['content']
                logger.info(f"Successfully generated summary ({len(summary)} characters)")
                return summary
            else:
                logger.error(f"Unexpected API response format: {result}")
                return None
        
        except requests.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            return None
    
    def fallback_summarization(self, transcript, sentences=5):
        """
        Fallback summarization method if API fails.
        
        Args:
            transcript (str): The transcript text
            sentences (int, optional): Number of sentences to include. Defaults to 5.
            
        Returns:
            str: Simple extractive summary
        """
        logger.info("Using fallback summarization method")
        
        # Split into sentences (simple approach)
        import re
        sentence_endings = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences_list = re.split(sentence_endings, transcript)
        
        # Take first few sentences as summary
        if len(sentences_list) <= sentences:
            return transcript
        
        summary = ' '.join(sentences_list[:sentences])
        logger.info(f"Generated fallback summary ({len(summary)} characters)")
        
        return summary + "\n\n(Note: This is a simple extractive summary generated as a fallback.)"
    
    def summarize_transcript(self, transcript):
        """
        Main function to summarize transcript.
        
        Args:
            transcript (str): The transcript text
            
        Returns:
            str: Summarized text
        """
        if not transcript:
            logger.error("Cannot summarize: No transcript provided")
            return None
        
        logger.info(f"Summarizing transcript ({len(transcript)} characters)")
        
        # Create prompt
        messages = self.create_summary_prompt(transcript)
        
        # Try to summarize with LLM
        summary = self.summarize_with_llm(messages)
        
        # Use fallback if LLM fails
        if not summary:
            logger.warning("LLM summarization failed, using fallback method")
            summary = self.fallback_summarization(transcript)
        
        return summary
