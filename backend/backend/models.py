from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import datetime

# Create a declarative base for SQLAlchemy models
Base = declarative_base()

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
