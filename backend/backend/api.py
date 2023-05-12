from fastapi import FastAPI, Depends
from .database import get_db
from .models import ChatMessage, ChatMessageCreate, ChatMessageResponse
from .websocket import websocket_endpoint
from starlette.websockets import WebSocket
from typing import List
from sqlalchemy.orm import Session

app = FastAPI()


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)


@app.get("/api/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).all()
    return messages


@app.post("/api/messages", response_model=ChatMessageResponse)
async def create_chat_message(
    message: ChatMessageCreate,
    db: Session = Depends(get_db),
):
    chat_message = ChatMessage(username=message.username, message=message.message)
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message
