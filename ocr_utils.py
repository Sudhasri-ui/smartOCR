import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def extract_text_from_pdf(pdf_path):
    uploaded_file = client.files.upload(file=pdf_path)
    response = client.models.generate_content(model='gemini-2.5-flash', contents=[uploaded_file, 'Extract ALL text from this document.'])
    client.files.delete(name=uploaded_file.name)
    return response.text.strip()

def extract_sheet_info(text):
    info = {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        if ':' in line:
            left, right = line.split(':', 1)
            if 2 < len(left) < 40 and 1 < len(right) < 60:
                info[left.strip().title()] = right.strip()
    return info

def extract_table_rows(text):
    return []
