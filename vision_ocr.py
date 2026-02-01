# vision_ocr.py
from google.cloud import vision
from google.oauth2 import service_account
import io, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "google_key.json")

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = vision.ImageAnnotatorClient(credentials=credentials)

def extract_text_from_file(file_path: str):
    with io.open(file_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    return response.full_text_annotation.text
