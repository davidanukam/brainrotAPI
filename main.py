from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

### CRUD Operations / HTTP Requests ###
# Create - POST
# Read - GET
# Update - PUT
# Create - DELETE

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float