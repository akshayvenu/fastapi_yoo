from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SessionCreate(BaseModel):
    gym_name: str

class SessionDB(BaseModel):
    session_id: str
    gym_name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)