'''
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")

# Configure the API key
genai.configure(api_key=api_key)

def structure_text(raw_text):
    """
    Takes raw OCR text and structures it into a standardized JSON format
    with fixed keys for PDF parsing.
    """
    
    # Define the prompt for structuring the text
    prompt = f"""
You are an expert document parser. Extract information from the following text and structure it into a JSON format.

The output MUST be a valid JSON object with these exact keys (use empty string "" if information is not found):

**Technician Details:**
- "technician_name": Name of the technician/employee
- "employee_id": Employee ID number
- "date": Date of the reading/work
- "route_zone": Route or Zone information
- "start_time": Start time of work
- "end_time": End time of work

**Summary Statistics:**
- "total_assigned": Total meters/tasks assigned
- "meters_read": Number of meters read/completed
- "no_access": Number of locations with no access
- "faulty_meters": Number of faulty meters found
- "reports_filed": Number of reports filed

**Additional Information:**
- "document_type": type of document (e.g., "Meter Reading Sheet", "Work Order", etc.)
- "notes": any additional notes or remarks

Raw text from document:
{raw_text}

Return ONLY the JSON object, no markdown formatting, no explanations, just pure JSON.
"""

    try:
        # Use the working model from your API
        print("Using model: models/gemini-2.5-flash")
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        print("✓ Successfully got response from Gemini")
        
        # Extract the response text
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse the JSON response
        structured_data = json.loads(response_text)
        
        # Ensure all required keys exist
        required_keys = [
            "technician_name", "employee_id", "date", "route_zone", 
            "start_time", "end_time", "total_assigned", "meters_read",
            "no_access", "faulty_meters", "reports_filed",
            "document_type", "notes"
        ]
        
        for key in required_keys:
            if key not in structured_data:
                structured_data[key] = ""
        
        return structured_data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return default structure on error
        return {
            "technician_name": "",
            "employee_id": "",
            "date": "",
            "route_zone": "",
            "start_time": "",
            "end_time": "",
            "total_assigned": "",
            "meters_read": "",
            "no_access": "",
            "faulty_meters": "",
            "reports_filed": "",
            "document_type": "",
            "notes": "Error parsing document structure"
        }
    
    except Exception as e:
        print(f"Error in structure_text: {e}")
        # Return default structure on error
        return {
            "technician_name": "",
            "employee_id": "",
            "date": "",
            "route_zone": "",
            "start_time": "",
            "end_time": "",
            "total_assigned": "",
            "meters_read": "",
            "no_access": "",
            "faulty_meters": "",
            "reports_filed": "",
            "document_type": "",
            "notes": f"Error: {str(e)}"
        }'''
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")

# Configure the API key
genai.configure(api_key=api_key)

def structure_text(raw_text):
    """
    Takes raw OCR text and structures it into a standardized JSON format
    with fixed keys for PDF parsing.
    """
    
    print(f"\n{'='*60}")
    print("STRUCTURE_TEXT CALLED")
    print(f"Raw text length: {len(raw_text)}")
    print(f"Raw text preview (first 200 chars):\n{raw_text[:200]}")
    print(f"{'='*60}\n")
    
    # Define the prompt for structuring the text
    prompt = f"""
You are an expert document parser. Extract information from the following meter reading sheet.

Extract and return a JSON object with these EXACT keys:

1. HEADER INFORMATION:
   - "technician_name": The technician's name
   - "employee_id": Employee/Tech ID number
   - "date": Date of reading
   - "route_zone": Route or Zone number
   - "start_time": Start time
   - "end_time": End time

2. SUMMARY STATISTICS:
   - "total_assigned": Total meters assigned
   - "meters_read": Number of meters read
   - "no_access": Number with no access
   - "faulty_meters": Number of faulty meters
   - "reports_filed": Reports filed count

3. PROPERTY DETAILS TABLE (CRITICAL - Extract ALL rows):
   - "property_grid": This is an ARRAY of objects. Extract EVERY row from the property/meter details table.
   
   Each row object must have ALL these fields:
   {{
     "address": "Street address or property location",
     "account_holder": "Name of account holder/owner",
     "meter_type": "Type of meter (Electric/Water/Gas)",
     "meter_no": "Meter number/ID",
     "previous_reading": "Previous reading value",
     "current_reading": "Current reading value", 
     "units": "Units consumed (difference)",
     "status": "Status (OK/No Access/Faulty/Accessible/Dog Present/etc)",
     "photo": "Photo status (Yes/No or other indicator)"
   }}

   IMPORTANT: Look for tables with columns like:
   - Address, Account Holder, Meter Type, Meter No, Previous Reading, Current Reading, Units, Status
   - Extract EVERY column you find
   - Extract EVERY row, even if there are 10, 20, or 50 rows

4. ADDITIONAL:
   - "document_type": Document type
   - "notes": Any field notes or remarks

Document text:
{raw_text}

Return ONLY valid JSON. No markdown, no explanations.
"""

    try:
        # Use the working model from your API
        print("Using model: models/gemini-2.5-flash")
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        print("✓ Successfully got response from Gemini")
        
        # Extract the response text
        response_text = response.text.strip()
        print(f"\nGemini response (first 500 chars):\n{response_text[:500]}\n")
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse the JSON response
        structured_data = json.loads(response_text)
        print(f"✓ Parsed JSON successfully")
        print(f"Structured data keys: {list(structured_data.keys())}")
        
        # Flatten nested structure if Gemini returned nested format
        if 'HEADER INFORMATION' in structured_data:
            # Extract from nested structure
            header = structured_data.get('HEADER INFORMATION', {})
            summary = structured_data.get('SUMMARY STATISTICS', {})
            property_table = structured_data.get('PROPERTY DETAILS TABLE', {})
            additional = structured_data.get('ADDITIONAL', {})
            
            # Flatten into expected format
            structured_data = {
                'technician_name': header.get('technician_name', ''),
                'employee_id': header.get('employee_id', ''),
                'date': header.get('date', ''),
                'route_zone': header.get('route_zone', ''),
                'start_time': header.get('start_time', ''),
                'end_time': header.get('end_time', ''),
                'total_assigned': summary.get('total_assigned', ''),
                'meters_read': summary.get('meters_read', ''),
                'no_access': summary.get('no_access', ''),
                'faulty_meters': summary.get('faulty_meters', ''),
                'reports_filed': summary.get('reports_filed', ''),
                'property_grid': property_table.get('property_grid', []),
                'document_type': additional.get('document_type', ''),
                'notes': additional.get('notes', '')
            }
            print(f"✓ Flattened nested structure")
        
        # Ensure all required keys exist
        required_keys = [
            "technician_name", "employee_id", "date", "route_zone", 
            "start_time", "end_time", "total_assigned", "meters_read",
            "no_access", "faulty_meters", "reports_filed",
            "document_type", "notes", "property_grid"
        ]
        
        for key in required_keys:
            if key not in structured_data:
                structured_data[key] = [] if key == "property_grid" else ""
        
        # Log property grid info
        if "property_grid" in structured_data:
            print(f"✓ Property Grid: {len(structured_data['property_grid'])} rows extracted")
        
        print(f"✓ Returning structured data\n")
        return structured_data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return {
            "technician_name": "",
            "employee_id": "",
            "date": "",
            "route_zone": "",
            "start_time": "",
            "end_time": "",
            "total_assigned": "",
            "meters_read": "",
            "no_access": "",
            "faulty_meters": "",
            "reports_filed": "",
            "document_type": "",
            "notes": "Error parsing document structure",
            "property_grid": []
        }
    
    except Exception as e:
        print(f"Error in structure_text: {e}")
        return {
            "technician_name": "",
            "employee_id": "",
            "date": "",
            "route_zone": "",
            "start_time": "",
            "end_time": "",
            "total_assigned": "",
            "meters_read": "",
            "no_access": "",
            "faulty_meters": "",
            "reports_filed": "",
            "document_type": "",
            "notes": f"Error: {str(e)}",
            "property_grid": []
        }