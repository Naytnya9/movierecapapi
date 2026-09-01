import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(
    title="Movie Recap API",
    description="AI Movie Recap Generator"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


class RecapTextRequest(BaseModel):
    transcript: str
    language: str = "Myanmar"
    length: str = "3 minutes"


@app.get("/")
def home():
    return {
        "message": "Movie Recap API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "openai_key_configured": bool(OPENAI_API_KEY)
    }


@app.post("/generate-recap-from-text")
def generate_recap_from_text(request: RecapTextRequest):

    try:

        if not OPENAI_API_KEY:
            return {
                "success": False,
                "error": "OPENAI_API_KEY is not configured in Render."
            }

        prompt = f"""
You are a professional movie recap script writer.

Create an engaging movie recap based ONLY on the transcript below.

Write the recap in {request.language} language.

Target length: approximately {request.length}.

Make it:
- Easy to understand
- Interesting and engaging
- Chronological
- Suitable for YouTube movie recap narration
- Do not invent important events that are not in the transcript

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

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
