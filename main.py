'''
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pdf_reader import extract_text_from_file
from gemini_structure import structure_text

import json

import os
import shutil
import re
from dotenv import load_dotenv


load_dotenv()  # 👈 THIS LINE IS CRITICAL

def safe_find(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else ""

# ✅ OCR + FIXED SCHEMA PARSER
#from gemini_ocr import extract_text_with_gemini

from llm_client import extract_structured_data

# ---------------- APP SETUP ----------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
templates = Jinja2Templates(directory="templates")

# ---------------- IN-MEMORY USERS ----------------
users = {"admin@example.com": "admin123"}

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return RedirectResponse("/login")

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in users and users[email] == password:
        request.session["user"] = email
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid email or password"}
    )

# ---------------- REGISTER ----------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(email: str = Form(...), password: str = Form(...)):
    users[email] = password
    return RedirectResponse("/login", status_code=303)

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "current_user": request.session["user"]}
    )

# ---------------- UPLOAD PDF ----------------
@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    request.session["pdf_path"] = pdf_path
    request.session["pdf_name"] = file.filename

    return RedirectResponse("/review", status_code=303)

# ---------------- REVIEW PAGE ----------------
@app.get("/review", response_class=HTMLResponse)
def review_page(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")

    pdf_name = request.session.get("pdf_name")
    if not pdf_name:
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse(
        "review.html",
        {
            "request": request,
            "pdf_url": f"/uploads/{pdf_name}",
            "current_user": request.session["user"]
        }
    )

# ---------------- 🔥 PARSE SHEET (FIXED TO RETURN JSON) ----------------
@app.post("/parse")
def parse_file(request: Request):
    file_path = request.session.get("pdf_path")

    if not file_path:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)

    try:
        # 1️⃣ OCR - Extract text from PDF
        raw_text = extract_text_from_file(file_path)
        
        # 2️⃣ Gemini structuring - Convert to structured JSON
        structured_data = structure_text(raw_text)
        
        # 3️⃣ Save to session for later use
        request.session["parsed_data"] = structured_data
        
        # 4️⃣ Return JSON response (NOT HTML template!)
        return JSONResponse(structured_data)
        
    except Exception as e:
        print(f"Error in /parse: {e}")
        return JSONResponse(
            {"error": str(e), "technician_name": "", "employee_id": "", "date": "",
             "route_zone": "", "start_time": "", "end_time": "", "total_assigned": "",
             "meters_read": "", "no_access": "", "faulty_meters": "", "reports_filed": "",
             "document_type": "", "notes": f"Error: {str(e)}"},
            status_code=500
        )

# ---------------- GET PARSED DATA ----------------
@app.get("/parsed-data")
def get_parsed_data(request: Request):
    return JSONResponse(request.session.get("parsed_data", {}))

# ---------------- SAVE ----------------
@app.post("/save")
def save_to_database(request: Request):
    data = request.session.get("parsed_data")
    if not data:
        return {"error": "No parsed data"}

    return {"status": "saved", "data": data}

# ---------------- LOGOUT ----------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
'''
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pdf_reader import extract_text_from_file
from gemini_structure import structure_text

import json

import os
import shutil
import re
from dotenv import load_dotenv


load_dotenv()  # 👈 THIS LINE IS CRITICAL

def safe_find(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else ""

# ✅ OCR + FIXED SCHEMA PARSER
#from gemini_ocr import extract_text_with_gemini

from llm_client import extract_structured_data

# ---------------- APP SETUP ----------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
templates = Jinja2Templates(directory="templates")

# ---------------- IN-MEMORY USERS ----------------
users = {"admin@example.com": "admin123"}

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return RedirectResponse("/login")

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in users and users[email] == password:
        request.session["user"] = email
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid email or password"}
    )

# ---------------- REGISTER ----------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(email: str = Form(...), password: str = Form(...)):
    users[email] = password
    return RedirectResponse("/login", status_code=303)

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "current_user": request.session["user"]}
    )

# ---------------- UPLOAD PDF ----------------
@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    request.session["pdf_path"] = pdf_path
    request.session["pdf_name"] = file.filename

    return RedirectResponse("/review", status_code=303)

# ---------------- REVIEW PAGE ----------------
@app.get("/review", response_class=HTMLResponse)
def review_page(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")

    pdf_name = request.session.get("pdf_name")
    if not pdf_name:
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse(
        "review.html",
        {
            "request": request,
            "pdf_url": f"/uploads/{pdf_name}",
            "current_user": request.session["user"]
        }
    )

# ---------------- 🔥 PARSE SHEET (FIXED TO RETURN JSON) ----------------
@app.post("/parse")
def parse_file(request: Request):
    file_path = request.session.get("pdf_path")

    if not file_path:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)

    try:
        print("\n" + "="*60)
        print("PARSE ENDPOINT CALLED")
        print(f"File path: {file_path}")
        print("="*60)
        
        # 1️⃣ OCR - Extract text from PDF
        print("Step 1: Extracting text from PDF...")
        raw_text = extract_text_from_file(file_path)
        print(f"✓ Extracted {len(raw_text)} characters")
        print(f"Text preview: {raw_text[:200]}")
        
        # 2️⃣ Gemini structuring - Convert to structured JSON
        print("\nStep 2: Structuring with Gemini...")
        structured_data = structure_text(raw_text)
        print(f"✓ Structured data created")
        print(f"Data keys: {list(structured_data.keys())}")
        print(f"Sample values:")
        print(f"  - technician_name: '{structured_data.get('technician_name')}'")
        print(f"  - employee_id: '{structured_data.get('employee_id')}'")
        print(f"  - date: '{structured_data.get('date')}'")
        
        # 3️⃣ Save to session for later use
        request.session["parsed_data"] = structured_data
        
        # 4️⃣ Return JSON response (NOT HTML template!)
        print(f"\nStep 3: Returning JSON response")
        print(f"Full response data: {structured_data}")
        print("="*60 + "\n")
        
        return JSONResponse(structured_data)
        
    except Exception as e:
        print(f"❌ ERROR in /parse: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"error": str(e), "technician_name": "", "employee_id": "", "date": "",
             "route_zone": "", "start_time": "", "end_time": "", "total_assigned": "",
             "meters_read": "", "no_access": "", "faulty_meters": "", "reports_filed": "",
             "document_type": "", "notes": f"Error: {str(e)}"},
            status_code=500
        )

# ---------------- GET PARSED DATA ----------------
@app.get("/parsed-data")
def get_parsed_data(request: Request):
    return JSONResponse(request.session.get("parsed_data", {}))

# ---------------- SAVE ----------------
from database import save_reading, get_all_readings, get_reading_by_id

@app.post("/save")
def save_to_database(request: Request):
    data = request.session.get("parsed_data")
    if not data:
        return JSONResponse({"error": "No parsed data"}, status_code=400)
    
    try:
        reading_id = save_reading(data)
        return JSONResponse({
            "status": "success", 
            "message": "Data saved successfully!",
            "id": reading_id
        })
    except Exception as e:
        print(f"Error saving: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# ---------------- REPORTS ----------------
@app.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")
    
    readings = get_all_readings()
    return templates.TemplateResponse(
        "reports.html",
        {"request": request, "readings": readings, "current_user": request.session["user"]}
    )

@app.get("/report/{reading_id}", response_class=HTMLResponse)
def view_report(request: Request, reading_id: int):
    if "user" not in request.session:
        return RedirectResponse("/login")
    
    reading = get_reading_by_id(reading_id)
    if not reading:
        return RedirectResponse("/reports")
    
    return templates.TemplateResponse(
        "report_detail.html",
        {"request": request, "reading": reading, "current_user": request.session["user"]}
    )

# ---------------- LOGOUT ----------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")