from fastapi import APIRouter, Depends, HTTPException
from app.models.transcript import TranscriptRequest
from app.api.yt_transcript import YoutubeTranscript

router = APIRouter(prefix="/transcript", tags=["transcript"])

def get_transcript_handler():
    return YoutubeTranscript()

@router.post("/save")
def save_transcript(
    request: TranscriptRequest,
    transcript_handler: YoutubeTranscript = Depends(get_transcript_handler),
):
    