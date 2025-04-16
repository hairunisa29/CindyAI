import yt_dlp
import requests
import os
import re

class YoutubeTranscript:
    def __init__(self):
        self.yt_dlp = yt_dlp.YoutubeDL()
        
    def get_transcript_url(self, video_url, lang="id"):
        ydl_opts = {
            'writesubtitles': True, 
            'writeautomaticsub': True,
            'subtitleslangs': [lang],
            'skip_download': True, 
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=False)
                
                # Check both manual and auto-generated subtitles
                for source in ["subtitles", "automatic_captions"]:
                    subtitles = info.get(source, {}).get(lang, [])
                    
                    # Get first available subtitle URL with supported format
                    for subtitle in subtitles:
                        if subtitle.get('ext') in ['srv1', 'vtt', 'ttml']:
                            return info.get("id"), subtitle['url']
                            
            except Exception as e:
                print(f"Error: {e}")
        
        return None, None
    
transcript_handler = YoutubeTranscript()

video_url = "https://www.youtube.com/watch?v=YTlJZNMH_7A"
video_info = transcript_handler.get_transcript_url(video_url)
print(f"Video Info: {video_info}")