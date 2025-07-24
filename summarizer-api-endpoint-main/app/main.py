import os
import tempfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import router

app = FastAPI()

# Serve static audio files from system temp directory
temp_dir = tempfile.gettempdir()
app.mount("/audio", StaticFiles(directory=temp_dir), name="audio")

# Enable CORS for frontend on port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or use ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your routes
app.include_router(router)