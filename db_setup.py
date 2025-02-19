"""
db_setup.py

Initializes the database using SQLAlchemy.
We create a ChatLog table to store user messages and AI responses.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# For SQLite, a local file named chat_logs.db:
DATABASE_URL = "sqlite:///./chat_logs.db"

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="anonymous")
    message = Column(Text, nullable=False)     # The user's message
    response = Column(Text, nullable=True)     # The AI's response
    mode = Column(String, default="just_chat") # "just_chat", "topic", "diagnosis", etc.
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the engine and session factory
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Creates the tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Run this file directly to initialize the database
    init_db()
    print("Database initialized!")
