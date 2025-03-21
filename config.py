import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "youtube_summarizer.log")

# Configure logging
def setup_logging():
    """Set up logging configuration."""
    numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Create a sample .env file if it doesn't exist
def create_sample_env():
    """Create a sample .env file if it doesn't exist."""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("""# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=youtube_summarizer.log
""")
        print("Created sample .env file. Please edit it with your API keys.")

# Initialize
logger = setup_logging()
create_sample_env()
