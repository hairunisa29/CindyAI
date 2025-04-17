import yt_dlp
import requests
import os
import re

class YoutubeTranscript:
    def __init__(self):
        self.yt_dlp = yt_dlp.YoutubeDL()
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.TRANSCRIPT_DIR = os.path.join(self.BASE_DIR, "transcript_files")
        
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
    
    def save_transcript(self, video_id, transcript_url):
        response = requests.get(transcript_url)

        if response.status_code == 200:
            transcript_text = ' '.join(re.findall(r'<text[^>]*>(.*?)</text>', response.text))
            
            file_path = os.path.join(self.TRANSCRIPT_DIR, video_id)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(transcript_text)
            print(f"Transcript saved: {file_path}")
        else:
            print("Failed to download transcript.")
    
transcript_handler = YoutubeTranscript()

video_url = "https://www.youtube.com/watch?v=YTlJZNMH_7A"
video_id, transcript_url = transcript_handler.get_transcript_url(video_url)
print(type(video_id))
# transcript = transcript_handler.save_transcript(video_id, transcript_url)
# print(transcript)