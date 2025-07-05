import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

model = genai.GenerativeModel(
    model_name = "gemini-2.0-flash",
    generation_config=generation_config,
)

def GenerateResponse(input, history=[]):
    prompt_parts = []
    for pair in history:
        prompt_parts.append(f"user: {pair['user']}")
        prompt_parts.append(f"assistant: {pair['assistant']}")

    prompt_parts.append(f"user: {input}")
    prompt_parts.append("assistant:")

    response = model.generate_content(prompt_parts)
    return response.text