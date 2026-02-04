from fastapi import FastAPI, HTTPException 
from bson import ObjectId
from typing import List, Optional 
from pydantic import BaseModel ,Field
from database import collection
from middleware.rate_limiter import rate_limiter


class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = Field(default = None,ge=0,le=120)




app = FastAPI()
app.middleware("http")(rate_limiter)


@app.post("/users/", response_model=dict)
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {
        "message": "User created successfully",
        "user": user.dict()
    }


@app.get("/get_users/", response_model=List[dict])
async def get_all_users():
    users = []
    async for user in collection.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        })
    return users



@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user id")

    user = await collection.find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["id"] = str(user.pop("_id"))
    return user



@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    try:
        result = await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user.dict()}
        )
        if result.modified_count == 1:
            return {"message": "User updated successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")



