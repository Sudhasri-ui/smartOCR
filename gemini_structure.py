import os, json, time
from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
DEFAULT = {'technician_name':'','employee_id':'','date':'','route_zone':'','start_time':'','end_time':'','total_assigned':'','meters_read':'','no_access':'','faulty_meters':'','reports_filed':'','document_type':'','notes':'','property_grid':[]}
def structure_text(raw_text):
    prompt = f'Extract info and return ONLY valid JSON with keys: technician_name, employee_id, date, route_zone, start_time, end_time, total_assigned, meters_read, no_access, faulty_meters, reports_filed, document_type, notes, property_grid (array). No markdown. Document: {raw_text}'
    for attempt in range(3):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            text = response.text.strip()
            start = text.find('{')
            end = text.rfind('}') + 1
            result = json.loads(text[start:end])
            for k in DEFAULT: result.setdefault(k, DEFAULT[k])
            return result
        except Exception as e:
            print(f'Attempt {attempt+1} failed: {e}')
            time.sleep(5)
    d = DEFAULT.copy()
    d['notes'] = 'Failed after 3 attempts'
    return d




