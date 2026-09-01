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
from pydantic import BaseModel
from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


class RecapTextRequest(BaseModel):
    transcript: str
    language: str = "Myanmar"
    length: str = "3 minutes"


@app.post("/generate-recap-from-text")
def generate_recap_from_text(request: RecapTextRequest):

    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured."
        )

    prompt = f"""
Create a movie recap script based on the following transcript.

Language: {request.language}
Target length: {request.length}

Make the recap:
- Easy to understand
- Interesting and engaging
- Written like a movie recap narrator
- Chronological
- Do not add information not supported by the transcript

Transcript:
{request.transcript}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {
        "success": True,
        "recap": response.output_text
    }
