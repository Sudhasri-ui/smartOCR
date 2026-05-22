import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔥 GEMINI OCR FILE LOADED 🔥")

def extract_text_from_file(file_path: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    response = model.generate_content([
        "Extract all readable text from this document clearly.",
        file_bytes
    ])

    return response.text

