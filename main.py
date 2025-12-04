from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

### CRUD Operations / HTTP Requests ###
# Create - POST
# Read - GET
# Update - PUT
# Create - DELETE

app = FastAPI()
app.title="BrainrotAPI"

# Database setup
engine = create_engine("sqlite:///brainrots.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Brainrot(Base):
    __tablename__="Brainrots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False, unique=True)
    value = Column(String(100), nullable=False)

# Link Database Model to the Engine
Base.metadata.create_all(engine)

# Pydantic Models (Dataclass)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

# Endpoints
@app.get("/")
def root():
    return {"message" : "learning"}