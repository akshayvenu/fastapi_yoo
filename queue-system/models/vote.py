from pydantic import BaseModel

class Vote(BaseModel):
    song_id: str
    user_id: str