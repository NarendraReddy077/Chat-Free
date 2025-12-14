import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from memory_store import get_chat_history, add_message

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1,
    streaming=True,
)


def build_prompt(history, user_message: str) -> str:
    prompt = (
        "You are a helpful and friendly AI chat assistant. "
        "Keep responses concise and conversational.\n\n"
    )
    recent_history = history[-10:] if len(history) > 10 else history
    for msg in recent_history:
        role = msg.get("role", "").capitalize()
        content = msg.get("content", "")
        prompt += f"{role}: {content}\n"
    prompt += f"\nUser: {user_message}\nAssistant:"
    return prompt


async def stream_response(session_id: str, user_message: str):
    history = get_chat_history(session_id)
    prompt = build_prompt(history, user_message)
    full_response = ""

    try:
        async for chunk in llm.astream(prompt):
            if chunk.content:
                full_response += chunk.content
                # Yield plain text tokens for SSE `onmessage`
                yield chunk.content

        # Persist history after streaming finishes
        add_message(session_id, "user", user_message)
        add_message(session_id, "assistant", full_response)

        # Signal end of stream to frontend
        yield {"event": "end", "data": "done"}
    except Exception as e:
        yield {"event": "error", "data": str(e)}
        