import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import re


# ---------------- OCR TEXT ----------------
def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text = ""

    for page in pages:
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2GRAY)
        page_text = pytesseract.image_to_string(img, config="--psm 6")
        text += page_text + "\n"

    return text.strip()


# ---------------- GENERIC SHEET INFO ----------------
def extract_sheet_info(text):
    info = {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    for line in lines:
        # CASE 1: label : value
        if ":" in line:
            left, right = line.split(":", 1)
            if 2 < len(left) < 40 and 1 < len(right) < 60:
                info[left.strip().title()] = right.strip()

        # CASE 2: label   value (spaces)
        elif re.search(r"\s{3,}", line):
            parts = re.split(r"\s{3,}", line)
            if len(parts) == 2:
                key, value = parts
                if 2 < len(key) < 40 and 1 < len(value) < 60:
                    info[key.strip().title()] = value.strip()

    return info


# ---------------- GENERIC TABLE DETECTION ----------------
def extract_table_rows(text):
    rows = []
    lines = [l for l in text.splitlines() if l.strip()]

    for line in lines:
        # Detect table-like rows (multiple columns)
        if re.search(r"\s{2,}", line) and any(char.isdigit() for char in line):
            cols = re.split(r"\s{2,}", line)
            if len(cols) >= 3:
                rows.append([c.strip() for c in cols])

    # Normalize column length
    if rows:
        max_len = max(len(r) for r in rows)
        for r in rows:
            while len(r) < max_len:
                r.append("")
    return rows
