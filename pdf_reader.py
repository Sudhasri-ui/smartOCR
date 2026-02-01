import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

def extract_text_from_file(file_path):
    """
    Extract text from PDF using Gemini Vision API
    Works for both text PDFs and scanned/image PDFs
    """
    print(f"\n{'='*60}")
    print(f"GEMINI VISION PDF EXTRACTION")
    print(f"File: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        print("📤 Uploading PDF to Gemini...")
        
        # Upload the PDF file to Gemini
        uploaded_file = genai.upload_file(file_path)
        print(f"✓ File uploaded: {uploaded_file.name}")
        print(f"  MIME type: {uploaded_file.mime_type}")
        
        # Create prompt for text extraction
        prompt = """
Extract ALL text from this document. 

Please extract:
1. All visible text, numbers, and data
2. Maintain the structure and formatting as much as possible
3. Include all sections: headers, body text, tables, notes, etc.

Return the complete extracted text without any additional commentary or formatting.
"""
        
        print("\n🤖 Processing with Gemini Vision...")
        
        # Use Gemini to extract text from the PDF
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content([uploaded_file, prompt])
        
        extracted_text = response.text.strip()
        
        print(f"✓ Gemini extracted {len(extracted_text)} characters")
        print(f"\nText preview (first 300 chars):")
        print("-" * 60)
        print(extracted_text[:300])
        print("-" * 60)
        print("="*60 + "\n")
        
        # Delete the uploaded file to save quota
        genai.delete_file(uploaded_file.name)
        print("✓ Cleaned up uploaded file\n")
        
        return extracted_text
        
    except Exception as e:
        print(f"❌ Error extracting text with Gemini: {e}")
        import traceback
        traceback.print_exc()
        return f"ERROR: Failed to extract text - {str(e)}"