import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from google.generativeai.types import GenerateContentResponse, GenerationConfig
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
        response = await model.generate_content_async(prompt.prompt)
        generated_text = response.text.strip().replace('*', '')
        return {"text": generated_text}
    except Exception as e:
        print(f"Error generating text: {e}")
        return {"error": "Failed to generate text"}

@app.post("/generate-image")
async def generate_image(prompt: TextPrompt):
    try:
        response: GenerateContentResponse = await genai.GenerativeModel(
            "gemini-1.5-flash"
        ).generate_content_async(
            contents=prompt.prompt,
            generation_config=GenerationConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        image_data = None
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    break
        
        if image_data:
            base64_image = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:image/png;base64,{base64_image}"
            return {"image_url": image_url}
        else:
            return {"error": "The AI did not return an image. Please try a different prompt."}

    except Exception as e:
        print("\n--- IMAGE GENERATION ERROR ---")
        traceback.print_exc()
        print("------------------------------\n")
        return {"error": "Failed to generate image. The model may not be available, or an API error occurred."}

@app.post("/generate-video")
async def generate_video(prompt: TextPrompt):
    video_url = "https://videos.pexels.com/video-files/3209828/3209828-hd_1280_720_25fps.mp4"
    return {"video_url": video_url}

# All other complex endpoints are temporarily removed to ensure the server starts.
# We can restore them after this test is successful. 