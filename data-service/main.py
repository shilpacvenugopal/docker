# data-service/main.py
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import os
import secrets
import logging
import requests  # Import requests library for making HTTP requests
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./users.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    current_token = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

Base.metadata.create_all(bind=engine)

class Token(BaseModel):
    access_token: str
    token_type: str

def create_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class CreateUser(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

logger = logging.getLogger(__name__)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging_service_url = "http://logging-service:80/log"

def log_activity(activity: str, username: str):
    log_data = {"activity": activity, "username": username}
    requests.post(logging_service_url, json=log_data)

@app.post("/register", response_model=UserResponse)
def register(user_data: CreateUser):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = password_context.hash(user_data.password)

        new_user = User(username=user_data.username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        log_activity("register", new_user.username)

        return UserResponse(username=new_user.username)
    except Exception as e:
        logger.error(f"Exception during registration: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()


@app.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    user = authenticate_user(username, password)
    
    if not user or not password_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.username)

    db = SessionLocal()
    user.current_token = token
    db.commit()
    db.close()

    log_activity("login", user.username)

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user
