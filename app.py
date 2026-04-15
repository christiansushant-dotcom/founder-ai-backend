from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Query(BaseModel):
    topic: str
    mode: str

@app.post("/generate")
def generate(query: Query):

    # TEMP DUMMY CONTEXT (your database later)
    context = """
    Reflection of light is the bouncing back of light rays from a surface.
    Laws of reflection:
    1. Angle of incidence = Angle of reflection
    2. Incident ray, reflected ray and normal lie on same plane
    """

    prompt = f"""
    You are a strict academic AI.

    Rules:
    - Answer ONLY from context
    - If not found → say 'Not available in syllabus'

    Mode: {query.mode}
    Topic: {query.topic}

    Context:
    {context}
    """

    response = client.chat.completions.create(
        model="gpt-5.3",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"response": response.choices[0].message.content}
