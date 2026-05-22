from google.cloud import vision
from google.oauth2 import service_account
import os, re, json, tempfile
key_json = os.getenv('GOOGLE_KEY_JSON')
if key_json:
    key_dict = json.loads(key_json)
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(key_dict, tmp)
    tmp.close()
    KEY_PATH = tmp.name
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KEY_PATH = os.path.join(BASE_DIR, 'google_key.json')
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = vision.ImageAnnotatorClient(credentials=credentials)
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f: content = f.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message: raise Exception(response.error.message)
    return response.text_annotations[0].description if response.text_annotations else ''
def extract_structured_data(raw_text: str):
    return {'sheet_info': {}, 'property_grid': []}
