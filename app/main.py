import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from app.endpoints import chat
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



app = FastAPI()

# Configure CORS with specific origins
origins = [
    "https://localhost:3000",
    "http://localhost:8000"
]

app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "FastAPI Config Test - Success!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)





#python -m app.main