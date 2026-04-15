from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request format
class Query(BaseModel):
    topic: str
    mode: str

# Dummy knowledge (RAG later)
def get_context(topic):
    return f"This is basic knowledge about {topic}."

# API endpoint
@app.post("/generate")
def generate_response(query: Query):
    context = get_context(query.topic)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": f"You are a teacher. Use this context: {context}"},
            {"role": "user", "content": f"Teach me about {query.topic} in {query.mode} mode"}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }

# Root route (IMPORTANT)
@app.get("/")
def root():
    return {"message": "Founder AI Backend Running 🚀"}
