from google.cloud import vision
from google.oauth2 import service_account
import os
import re

# -------- LOAD CREDENTIALS EXPLICITLY --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "google_key.json")

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

client = vision.ImageAnnotatorClient(credentials=credentials)

# -------- OCR FUNCTION --------
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    return response.text_annotations[0].description


# -------- FIELD MAP (KEYS SAME, VALUES DYNAMIC) --------
FIELD_MAP = {
    "technician_name": r"Technician\s*Name\s*[:\-]?\s*([A-Za-z .]+)",
    "employee_id": r"(Employee\s*ID|Employee\s*No)\s*[:\-]?\s*(\w+)",
    "date": r"Date\s*[:\-]?\s*([\d/.\-]+)",
    "route_zone": r"(Route|Zone|Route\s*/\s*Zone)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
    "total_assigned": r"Total\s*Assigned\s*[:\-]?\s*(\d+)",
    "meters_read": r"Meters\s*Read\s*[:\-]?\s*(\d+)",
    "no_access": r"No\s*Access\s*[:\-]?\s*(\d+)",
    "faulty_meters": r"Faulty\s*Meters\s*[:\-]?\s*(\d+)",
}



# -------- STRUCTURED EXTRACTION --------
import re

def extract_structured_data(raw_text: str):
    data = {
        "sheet_info": {},
        "property_grid": []
    }

    # -------- SHEET INFO --------
    for key, pattern in FIELD_MAP.items():
        match = re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL)
        data["sheet_info"][key] = match.group(1).strip() if match else ""

    # -------- PROPERTY TABLE --------
    lines = raw_text.splitlines()

    for line in lines:
        row = re.findall(
            r"([A-Za-z\s]+)\s+(ELECTRICITY|WATER)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(Accessible|No Access)\s+(Yes|No)",
            line,
            re.IGNORECASE
        )

        if row:
            acc, mtype, meter, prev, curr, units, access, photo = row[0]
            data["property_grid"].append({
                "account_holder": acc.strip(),
                "meter_type": mtype,
                "meter_no": meter,
                "previous_reading": prev,
                "current_reading": curr,
                "units_used": units,
                "access_status": access,
                "photo": photo
            })

    return data


