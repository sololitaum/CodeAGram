from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for the frontend (you can specify more strict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (can be restrictive in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request body model using Pydantic
class TranslateRequest(BaseModel):
    code: str
    source_language: str
    target_language: str

# Define the API route for translation
@app.post("/translate")
async def translate_code(request: TranslateRequest):
    # Set OpenAI API key
    openai.api_key = ''
    # Define the translation prompt
    prompt = f"Translate the following code from {request.source_language} to {request.target_language}:\n{request.code}"

    # Use OpenAI API to generate the translation
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the model you prefer (e.g., gpt-4)
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the translated code from the response
    translated_code = response['choices'][0]['message']['content'].strip()

    # Return the translated code
    return {"translated_code": translated_code}
