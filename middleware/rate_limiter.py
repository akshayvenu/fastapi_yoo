vimport time
from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT = 5
WINDOW = 60

rate_store = {}

async def rate_limiter(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    now = time.time()

    record = rate_store.get(ip)

    if not record:
        rate_store[ip] = {"count": 1, "start": now}
    else:
        elapsed = now - record["start"]

        if elapsed > WINDOW:
            rate_store[ip] = {"count": 1, "start": now}
        else:
            record["count"] += 1
            if record["count"] > RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"}
                )

    return await call_next(request)
