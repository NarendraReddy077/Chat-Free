from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from chat import stream_response

app = FastAPI(title="Chat Free", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/chat/stream")
async def chat_stream(
    session_id: str = Query(...),
    message: str = Query(..., max_length=2000),
):
    msg = message.strip()
    if not msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return EventSourceResponse(stream_response(session_id, msg))


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
