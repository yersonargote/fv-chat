from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from starlette.websockets import WebSocket, WebSocketDisconnect
import json
from fastapi import Depends
from sqlalchemy import Column, Integer, String, Text, DateTime

# Configuration for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

# Create a SQLAlchemy engine to manage database connections
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SQLAlchemy session factory to create new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for SQLAlchemy models
Base = declarative_base()

# Create a FastAPI app instance
app = FastAPI()

# Add middleware to handle database sessions
app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)

# Add middleware to handle Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Mount the static files directory for serving client-side code
# app.mount("/static", StaticFiles(directory="static"), name="static")


# Define a SQLAlchemy model for Chat messages
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Define a Pydantic model for creating new chat messages
class ChatMessageCreate(BaseModel):
    username: str
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    username: str
    message: str
    created_at: datetime


# Define a route for serving the index HTML file
# @app.get("/", response_class=HTMLResponse)
# async def index():
#     return open("static/index.html").read()


# Define a route for handling WebSocket connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Wait for new messages from the WebSocket
            data = await websocket.receive_text()

            # Parse the message data as a JSON object
            message = json.loads(data)

            # Create a new chat message in the database
            chat_message = ChatMessage(
                username=message["username"], message=message["message"]
            )
            db = SessionLocal()
            db.add(chat_message)
            db.commit()

            # Send the new chat message to all connected clients
            await websocket.send_json({"status": "ok", "message": message})
        except WebSocketDisconnect:
            break


# # Define a route for retrieving all chat messages
# @app.get("/api/messages", response_model=List[ChatMessageResponse])
# async def get_chat_messages(db: Session = Depends(get_db)):
#     return db.query(ChatMessage).all()


# @app.get("/api/messages", response_model=None)
@app.get("/api/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).all()
    return messages


# Define a route for creating new chat messages
# @app.post("/api/messages", response_model=None)
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
