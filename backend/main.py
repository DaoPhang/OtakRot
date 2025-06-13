from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TextPrompt(BaseModel):
    prompt: str

load_dotenv()

# Add explicit check for the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or "YOUR_API_KEY_HERE" in api_key:
    raise ValueError(
        "GEMINI_API_KEY not found or is not set correctly. "
        "Please make sure you have a .env file in the 'backend' directory "
        "with your actual API key, like 'GEMINI_API_KEY=AIz...'"
    )

genai.configure(api_key=api_key)

# Define the system instruction for the model
system_instruction = (
    "You are OtakRot, a deeply knowledgeable Malaysian meme generator. Your humor is sharp, witty, and hyperlocal. "
    "Your core purpose is to generate meme captions that resonate strongly with Malaysians. "
    "Your responses MUST be in casual Manglish. Use common slang like 'lah', 'wei', 'kantoi', 'syok', 'bosan gila' frequently and appropriately. "
    "Base your humor on shared Malaysian experiences: the pain of KL traffic jams, the joy of public holidays, the love for food like Nasi Lemak and Durian, mamak culture, and dealing with sudden tropical rainstorms. "
    "Keep every caption under 20 words. Be funny, be relatable, be Malaysian."
)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instruction
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the OtakRot API!"}

@app.post("/generate-text")
async def generate_text(prompt: TextPrompt):
    try:
        # The system instruction is already set, so we just send the user's prompt.
        response = await model.generate_content_async(prompt.prompt)
        
        # Clean up the response text
        generated_text = response.text.strip().replace('*', '')
        
        return {"text": generated_text}
    except Exception as e:
        print(f"Error generating text: {e}")
        return {"error": "Failed to generate text"} 