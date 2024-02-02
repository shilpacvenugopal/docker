from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
import secrets
import os
from jose import jwt, JWTError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"

logging_service_url = "http://logging-service:80/log"

def log_activity(activity: str, username: str):
    log_data = {"activity": activity, "username": username}
    requests.post(logging_service_url, json=log_data)

class APIKeyResponse(BaseModel):
    api_key: str

@app.get("/generate-api-key", response_model=APIKeyResponse)
async def generate_api_key(current_user: str = Depends(oauth2_scheme)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    api_key = generate_random_api_key()
    return {"api_key": api_key}

def generate_random_api_key():
    return secrets.token_urlsafe(32)
