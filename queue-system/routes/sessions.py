from fastapi import APIRouter, HTTPException
from uuid import uuid4
from database import sessions, songs, votes
from models.session import SessionCreate

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/")
async def create_session(data: SessionCreate):
    session_id = str(uuid4())

    session = {
        "session_id": session_id,
        "gym_name": data.gym_name,
        "is_active": True
    }

    await sessions.insert_one(session)
    return {"session_id": session_id}

@router.get("/{session_id}")
async def get_session(session_id: str):
    session = await sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session["_id"] = str(session["_id"])
    return session

@router.get("/{session_id}/join")
async def join_session(session_id: str):
    session = await sessions.find_one({"session_id": session_id, "is_active": True})
    if not session:
        raise HTTPException(status_code=404, detail="Session inactive or not found")
    return {"message": "Joined session", "session_id": session_id}

@router.delete("/{session_id}")
async def delete_session(session_id: str):
    await sessions.delete_one({"session_id": session_id})
    await songs.delete_many({"session_id": session_id})
    await votes.delete_many({"session_id": session_id})
    return {"message": "Session ended and cleaned"}