import os 
import dotenv
from motor.motor_asyncio import AsyncIOMotorClient



dotenv.load_dotenv()

uri = os.getenv("MONGODB_URI")


client = AsyncIOMotorClient(uri)


db = client["fastapi_crud"] 
collection = db["users"] 


