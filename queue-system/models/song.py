from pydantic import BaseModel
from typing import Optional

class SongCreate(BaseModel):
    youtube_url: HttpUrl

class SongDB(BaseModel):
    song_id: str
    session_id: str
    youtube_url: str
    title: str
    duration: int
    votes: int = 0
    is_played: bool = False
    