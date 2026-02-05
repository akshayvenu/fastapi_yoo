from fastapi import APIRouter, HTTPException
from uuid import uuid4
from database import sessions, songs, votes
from models.song import SongCreate
from models.vote import Vote

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.post("/{session_id}/add")
async def add_song(session_id: str, data: SongCreate):

    # check session
    session = await sessions.find_one(
        {"session_id": session_id, "is_active": True}
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not active")

    song = {
        "song_id": str(uuid4()),
        "session_id": session_id,
        "youtube_url": data.youtube_url,
        "votes": 0,
        "is_played": False
    }

    await songs.insert_one(song)
    return {"message": "Song added", "song_id": song["song_id"]}



@router.get("/{session_id}/queue")
async def get_queue(session_id: str):

    queue = await songs.find(
        {"session_id": session_id, "is_played": False}
    ).sort("votes", -1).to_list(100)

    for song in queue:
        song["_id"] = str(song["_id"])

    return queue


@router.post("/vote")
async def vote_song(vote: Vote):

    existing = await votes.find_one({
        "song_id": vote.song_id,
        "user_id": vote.user_id
    })

    if existing:
        raise HTTPException(status_code=400, detail="Already voted")

    await votes.insert_one(vote.dict())

    await songs.update_one(
        {"song_id": vote.song_id, "is_played": False},
        {"$inc": {"votes": 1}}
    )

    return {"message": "Vote added"}


@router.delete("/vote")
async def remove_vote(vote: Vote):

    result = await votes.delete_one(vote.dict())

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vote not found")

    await songs.update_one(
        {"song_id": vote.song_id, "is_played": False},
        {"$inc": {"votes": -1}}
    )

    return {"message": "Vote removed"}



@router.get("/{session_id}/next")
async def next_song(session_id: str):

    song = await songs.find_one_and_update(
        {
            "session_id": session_id,
            "is_played": False
        },
        {
            "$set": {"is_played": True}
        },
        sort=[("votes", -1)]
    )

    if not song:
        return {"message": "No songs left"}

    song["_id"] = str(song["_id"])
    return song



@router.get("/{session_id}/current")
async def current_song(session_id: str):

    song = await songs.find_one(
        {"session_id": session_id, "is_played": True},
        sort=[("_id", -1)]
    )

    if not song:
        return {"message": "No song playing"}

    song["_id"] = str(song["_id"])
    return song