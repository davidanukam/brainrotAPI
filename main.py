from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, BLOB
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

# For development: allow all origins. Lock this down later.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # ["*"] allows any origin
    allow_credentials=False,    # keep False if you don't use cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine("sqlite:///brainrots.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Brainrot(Base):
    __tablename__="Brainrots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    value = Column(String, nullable=False)

# Link Database Model to the Engine
Base.metadata.create_all(engine)

# Pydantic Models (Dataclass)
class BrainrotCreate(BaseModel):
    name:str
    description:str
    image:str
    value:str

class BrainrotResponse(BaseModel):
    id:int
    name:str
    description:str
    image:str
    value:str
    
    class Config:
        from_attributes=True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def root():
    return {"message" : "learning"}

@app.get("/brainrots/", response_model=List[BrainrotResponse])
def get_all_brainrots(db: Session = Depends(get_db)):
    brainrots = db.query(Brainrot).all()
    return brainrots

@app.get("/brainrots/{brainrot_id}", response_model=BrainrotResponse)
def get_brainrot(brainrot_id: int, db: Session = Depends(get_db)):
    brainrot = db.query(Brainrot).filter(Brainrot.id == brainrot_id).first()
    if not brainrot:
        raise HTTPException(status_code=404, detail="Brainrot not found!")
    return brainrot

@app.post("/brainrots/", response_model=BrainrotResponse)
def create_brainrot(brainrot: BrainrotCreate, db: Session = Depends(get_db)):
    if db.query(Brainrot).filter(Brainrot.name == brainrot.name).first():
        raise HTTPException(status_code=404, detail="Brainrot already exists!")
    
    new_brainrot = Brainrot(**brainrot.model_dump())
    db.add(new_brainrot)
    db.commit()
    db.refresh(new_brainrot)
    return new_brainrot

@app.put("/brainrots/{brainrot_id}", response_model=BrainrotResponse)
def update_brainrot(brainrot_id: int, brainrot: BrainrotCreate, db: Session = Depends(get_db)):
    found_brainrot = db.query(Brainrot).filter(Brainrot.id == brainrot_id).first()
    if not brainrot:
        raise HTTPException(status_code=404, detail="Brainrot not found!")
    
    for field, value in brainrot.model_dump().items():
        setattr(found_brainrot, field, value)
    
    db.commit()
    db.refresh(found_brainrot)
    return found_brainrot

@app.delete("/brainrots/{brainrot_id}", response_model=BrainrotResponse)
def delete_brainrot(brainrot_id: int, db: Session = Depends(get_db)):
    brainrot = db.query(Brainrot).filter(Brainrot.id == brainrot_id).first()
    if not brainrot:
        raise HTTPException(status_code=404, detail="Brainrot not found!")
    db.commit()
    db.delete(brainrot)
    return brainrot