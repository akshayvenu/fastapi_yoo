
from fastapi import FastAPI
from database import sessions, songs, votes
from routes.song import router as song_router
from routes.sessions import router as session_router
from middleware.rate_limiter import rate_limiter

app = FastAPI()

app.middleware("http")(rate_limiter)

app.include_router(session_router)
app.include_router(song_router)

