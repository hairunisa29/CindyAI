"""YouTube utilities for handling video transcripts and metadata."""
from typing import Dict, Optional
import yt_dlp
import requests
import os
import re
import json
import logging

logger = logging.getLogger(__name__)
# Set logging level to DEBUG for more detailed output
logger.setLevel(logging.DEBUG)

# Define transcript directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcript_files")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)  # Ensure directory exists

class YouTubeTranscriptExtractor:
    def __init__(self):
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'srv1/vtt/ttml',
            'subtitleslangs': ['id'],
            'skip_download': True,
            'quiet': True,
            'no_warnings': True
        }

    def get_video_id(self, video_url: str) -> Optional[str]:
        """Extract video ID from a YouTube URL."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                return ydl.extract_info(video_url, download=False).get("id")
        except Exception as e:
            logger.error(f"Error getting video ID: {e}")
            return None

    def get_transcript_url(self, video_url: str) -> tuple[Optional[str], Optional[str]]:
        """Retrieve transcript URL (manual or auto-generated)."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                for key in ["subtitles", "automatic_captions"]:
                    if 'id' in info.get(key, {}):
                        for fmt in info[key]['id']:
                            if fmt.get('ext') in ['srv1', 'vtt', 'ttml']:
                                return info.get("id"), fmt['url']
            return None, None
        except Exception as e:
            logger.error(f"Error getting transcript URL: {e}")
            return None, None

    def extract_transcript(self, video_url: str) -> Optional[str]:
        """Extract transcript from a YouTube video."""
        try:
            video_id, transcript_url = self.get_transcript_url(video_url)
            if not transcript_url:
                logger.warning("No transcript URL found")
                return None

            response = requests.get(transcript_url)
            if response.status_code == 200:
                transcript_text = ' '.join(re.findall(r'<text[^>]*>(.*?)</text>', response.text))
                if transcript_text:
                    logger.debug(f"Successfully extracted transcript for video {video_id}")
                    return transcript_text
                else:
                    logger.warning("No text found in transcript")
            else:
                logger.error(f"Failed to download transcript: {response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            return None

    def get_video_metadata(self, video_url: str) -> Optional[Dict]:
        """Get metadata for a YouTube video."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date')
                }
        except Exception as e:
            logger.error(f"Error getting metadata for {video_url}: {str(e)}")
            return None

    def _process_subtitles(self, subtitles: Dict) -> str:
        """
        Process subtitles into clean text.
        
        Args:
            subtitles: Raw subtitle data
            
        Returns:
            str: Cleaned transcript text
        """
        try:
            # Parse JSON subtitles
            logger.debug("Parsing JSON subtitle data")
            subtitle_data = json.loads(subtitles['data'])
            
            # Extract and join text from each subtitle entry
            transcript_parts = []
            for event in subtitle_data.get('events', []):
                if 'segs' in event:
                    for seg in event['segs']:
                        if 'utf8' in seg:
                            text = seg['utf8'].strip()
                            if text:  # Only add non-empty segments
                                transcript_parts.append(text)
            
            transcript = ' '.join(transcript_parts)
            logger.debug(f"Number of transcript segments: {len(transcript_parts)}")
            return transcript
            
        except Exception as e:
            logger.error(f"Error processing subtitles: {str(e)}", exc_info=True)
            return ""

# Example usage:
# extractor = YouTubeTranscriptExtractor()
# transcript = extractor.extract_transcript("https://www.youtube.com/watch?v=VIDEO_ID")
# metadata = extractor.get_video_metadata("https://www.youtube.com/watch?v=VIDEO_ID") 