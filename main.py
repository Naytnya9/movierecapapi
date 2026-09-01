from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RecapRequest(BaseModel):
    language: str
    length: str


@app.get("/")
def home():
    return {
        "message": "Movie Recap AI API is running!"
    }


@app.post("/generate-recap")
def generate_recap(request: RecapRequest):

    recap = f"""
🎬 Movie Recap

Language: {request.language}
Recap Length: {request.length}

This is a test movie recap.

The real AI-generated movie recap
will appear here later.
"""

    return {
        "success": True,
        "recap": recap
    }
