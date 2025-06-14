import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from google.generativeai.types import GenerateContentResponse, GenerationConfig
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client

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

# Configure Stability AI client
stability_api_key = os.getenv("STABILITY_API_KEY")
if not stability_api_key:
    raise ValueError("STABILITY_API_KEY not found in .env file.")

stability_client = client.StabilityInference(
    key=stability_api_key,
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

# Define the system instruction for the model
system_instruction = (
    "You are OtakRot, a deeply knowledgeable Malaysian meme generator. Your humor is sharp, witty, and hyperlocal. "
    "Your core purpose is to generate meme captions that resonate strongly with Malaysians. "
    "Your responses MUST be in casual Manglish. Use common slang like 'lah', 'wei', 'kantoi', 'syok', 'bosan gila' frequently and appropriately. "
    "Base your humor on shared Malaysian experiences: the pain of KL traffic jams, the joy of public holidays, the love for food like Nasi Lemak and Durian, mamak culture, and dealing with sudden tropical rainstorms. "
    "Keep every caption under 20 words. Be funny, be relatable, be Malaysian."
)

# Define a new system instruction for a prompt-enhancing model
image_prompt_enhancer_instruction = (
    "You are a creative assistant for a deeply knowledgeable Malaysian meme image generator. Your task is to take a simple user prompt "
    "and expand it into a rich, detailed, and visually descriptive prompt for Stable Diffusion. "
    "The expanded prompt must describe a vibrant, realistic photograph. It must faithfully include all key elements and concepts from the user's original prompt. "
    "The scene should have strong meme potential, focusing on exaggerated expressions and relatable situations. "
    "Describe the setting, the subjects, and the specific actions with high detail. The composition should be dramatic and clear, like a scene from a movie. "
    "The final prompt should be a single paragraph of descriptive text. Do not add any conversational text. "
    "The output must be only the prompt itself. For example, if the user says 'A man in a suit shaking hands while hiding a knife behind his back', you should output something like: "
    "'Cinematic still of two men in sharp business suits shaking hands in a modern, cold office. One man has a warm, trustworthy smile. The other man has a forced, slightly sinister smile, and his other hand, hidden behind his back, firmly grips a sleek, sharp knife. The focus is sharp, capturing the texture of the suits and the glint of the hidden blade. The lighting is dramatic, with deep shadows, creating a tense, suspenseful atmosphere.' "
)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instruction
)

# Create a separate model for enhancing image prompts
image_prompt_enhancer_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=image_prompt_enhancer_instruction
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
        # 1. Use Gemini to enhance the user's prompt
        enhancer_response = await image_prompt_enhancer_model.generate_content_async(prompt.prompt)
        enhanced_prompt = enhancer_response.text.strip()

        print(f"Enhanced Prompt: {enhanced_prompt}") # For debugging

        # 2. Use the enhanced prompt with the Stability AI client
        answers = stability_client.generate(
            prompt=enhanced_prompt,
            style_preset="photographic",
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    return {"error": "The prompt was flagged by the safety filter. Please try a different prompt."}
                if artifact.type == generation.ARTIFACT_IMAGE:
                    # Encode the raw image data into a Base64 string for the browser
                    base64_image = base64.b64encode(artifact.binary).decode("utf-8")
                    image_url = f"data:image/png;base64,{base64_image}"
                    return JSONResponse(content={"image_url": image_url})
        
        # If no image was returned for some reason
        return JSONResponse(content={"error": "The AI did not return an image."}, status_code=500)

    except Exception as e:
        print("\n--- STABILITY AI ERROR ---")
        traceback.print_exc()
        print("--------------------------\n")
        
        error_message = str(e)
        if hasattr(e, 'details'):
            error_message = e.details()

        return JSONResponse(content={"error": f"Stability AI Error: {error_message}"}, status_code=500)

# All other complex endpoints are temporarily removed to ensure the server starts.
# We can restore them after this test is successful. 