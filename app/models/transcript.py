from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    video_id: str
    transcript_url: str
