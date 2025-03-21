# YouTube Transcript Summarizer

A command-line tool that takes a YouTube URL, downloads the video transcript using youtube-transcript-api, summarizes it with a Large Language Model (LLM), and outputs the result as a Markdown (.md) file.

## Features

- Accepts YouTube URLs (both shortened `youtu.be` and standard `youtube.com` formats)
- Downloads video transcripts directly from YouTube using youtube-transcript-api
- Summarizes transcripts using OpenRouter API
- Saves summaries as Markdown files with metadata
- Supports multiple languages (defaults to English)
- Includes error handling and logging

## Requirements

- Python 3.6+
- Required packages (see `requirements.txt`):
  - requests
  - beautifulsoup4
  - openrouter
  - python-dotenv
  - youtube-transcript-api

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/youtube_summariser.git
   cd youtube_summariser
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_MODEL=openai/gpt-3.5-turbo
   ```

   You can get an API key from [OpenRouter](https://openrouter.ai/).

## Usage

### Basic Usage

Make sure your virtual environment is activated:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then run the script:

```bash
python youtube_summarizer.py https://youtu.be/dQw4w9WgXcQ
```

### Options

- `--language`, `-l`: Preferred transcript language (default: en)
- `--output`, `-o`: Custom output file path
- `--verbose`, `-v`: Enable verbose output

### Examples

```bash
# Summarize a video with default settings
python youtube_summarizer.py https://youtu.be/dQw4w9WgXcQ

# Specify a language
python youtube_summarizer.py https://youtu.be/dQw4w9WgXcQ --language fr

# Specify an output file
python youtube_summarizer.py https://youtu.be/dQw4w9WgXcQ --output my_summary.md

# Enable verbose output
python youtube_summarizer.py https://youtu.be/dQw4w9WgXcQ --verbose
```

## Output

The tool generates a Markdown file with the following structure:

```markdown
# Video Summary: [Video Title]

## Summary

[Generated summary of the video transcript]

## Metadata
- Original URL: [YouTube URL]
- Video ID: [Video ID]
- Processed on: [Date]
```

## Testing

Make sure your virtual environment is activated, then run the test script to verify the functionality:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python tests/test_summarizer.py
```

You can also run a simple test to check if the youtube-transcript-api is working correctly:

```bash
python test_youtube_api.py
```

## Troubleshooting

- **API Key Issues**: Ensure your OpenRouter API key is correctly set in the `.env` file.
- **Transcript Download Failures**: Some videos may not have transcripts available or have disabled transcripts.
- **Rate Limiting**: If you encounter rate limiting from the YouTube API or the LLM API, try again later.

## License

[MIT License](LICENSE)

## Acknowledgements

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for providing access to YouTube transcripts
- [OpenRouter](https://openrouter.ai/) for the LLM API
