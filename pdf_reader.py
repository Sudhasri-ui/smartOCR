import os, time
from google import genai
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
def extract_text_from_file(file_path):
    if not os.path.exists(file_path): raise FileNotFoundError(f'Not found: {file_path}')
    for attempt in range(3):
        try:
            print(f'Attempt {attempt+1}: Uploading...')
            uploaded_file = client.files.upload(file=file_path)
            response = client.models.generate_content(model='gemini-2.5-flash', contents=[uploaded_file, 'Extract ALL text from this document. Maintain structure.'])
            client.files.delete(name=uploaded_file.name)
            print(f'Extracted {len(response.text)} chars')
            return response.text.strip()
        except Exception as e:
            print(f'Attempt {attempt+1} failed: {e}')
            time.sleep(10)
    return 'ERROR: Failed after 3 attempts'




