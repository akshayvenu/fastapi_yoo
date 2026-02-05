import os
import dotenv
from motor.motor_asyncio import AsyncIOMotorClient


dotenv.load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("MONGODB_URI environment variable is not set")

client = AsyncIOMotorClient(uri)
db = client.gym_music

sessions = db.sessions
songs = db.songs
votes = db.votes