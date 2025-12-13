# Chat Free (AI Chat Assistant)

A simple full‑stack AI chatbot with a React frontend and a FastAPI backend that streams responses from Google Gemini.

## Features

- Modern full‑screen chat UI
- Live streaming responses (Server‑Sent Events)
- Per‑session chat history saved to JSON files
- Easy local setup and deployment

## Tech Stack

- Frontend: React, JavaScript, CSS
- Backend: FastAPI, Uvicorn
- AI: Google Gemini (via langchain-google-genai)
- Storage: Local JSON files

## Setup

### Backend

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install fastapi uvicorn[standard] sse-starlette python-dotenv langchain-google-genai
