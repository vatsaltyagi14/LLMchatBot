from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from db_setup import init_db, SessionLocal, ChatLog
from local_llm import LocalLLM  # This uses Ollama with llama3.2:3b

app = FastAPI(
    title="Mental Health Chatbot API",
    description="A local-LLM-based chatbot backend for mental health support.",
    version="0.1.0"
)

# Allow CORS for your React frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()
db_session = SessionLocal()

# Now create the LocalLLM with the same "llama3.2:3b" model you have
llm = LocalLLM(model_name="llama3.2:3b")

class ChatRequest(BaseModel):
    user_id: Optional[str] = "anonymous"
    message: str
    mode: Optional[str] = "just_chat"

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_req: ChatRequest):
    """
    Receives a user message, sends it to the Ollama-based LocalLLM,
    stores both user message and AI response in the DB, and returns the response.
    """
    # 1) Store user's message
    new_chat = ChatLog(
        user_id=chat_req.user_id,
        message=chat_req.message,
        mode=chat_req.mode
    )
    db_session.add(new_chat)
    db_session.commit()
    db_session.refresh(new_chat)

    # 2) Generate a response via Ollama's chat
    ai_response = llm.chat(chat_req.message)

    # 3) Save AI response back to the database
    new_chat.response = ai_response
    db_session.commit()

    # 4) Return the AI response
    return {"response": ai_response}

@app.get("/history")
def get_history(user_id: str = "anonymous"):
    """
    Retrieves all chat logs for a given user_id.
    Returns them in a simple list format.
    """
    chat_logs = (
        db_session.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .order_by(ChatLog.timestamp.asc())
        .all()
    )
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "message": log.message,
            "response": log.response,
            "mode": log.mode,
            "timestamp": log.timestamp
        }
        for log in chat_logs
    ]


@app.delete("/history")
def delete_history(user_id: str = Query("anonymous")):
    # Make sure 'ChatLog' is imported, and 'db_session' is available
    db_session.query(ChatLog).filter(ChatLog.user_id == user_id).delete()
    db_session.commit()
    return {"status": "ok", "message": f"History for '{user_id}' deleted"}


@app.on_event("shutdown")
def shutdown_event():
    """
    Close the database session when the server shuts down.
    """
    db_session.close()
