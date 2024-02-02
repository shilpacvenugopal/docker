from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

class LogEntry(BaseModel):
    activity: str
    username: str

logs = []

@app.post("/log")
async def log_activity(entry: LogEntry):
    logs.append(entry.dict())
    return {"status": "logged"}

@app.get("/logs", response_model=List[LogEntry])
async def get_logs():
    return logs
