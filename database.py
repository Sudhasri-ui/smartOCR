import sqlite3
import json
from datetime import datetime

DB_FILE = "meter_readings.db"

def init_database():
    """Initialize the database with tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table for sheet info
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technician_name TEXT,
            employee_id TEXT,
            date TEXT,
            route_zone TEXT,
            start_time TEXT,
            end_time TEXT,
            total_assigned TEXT,
            meters_read TEXT,
            no_access TEXT,
            faulty_meters TEXT,
            reports_filed TEXT,
            document_type TEXT,
            notes TEXT,
            property_grid TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

def save_reading(data):
    """Save a reading to the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Convert property_grid array to JSON string
    property_grid_json = json.dumps(data.get('property_grid', []))
    
    cursor.execute("""
        INSERT INTO readings (
            technician_name, employee_id, date, route_zone,
            start_time, end_time, total_assigned, meters_read,
            no_access, faulty_meters, reports_filed, document_type,
            notes, property_grid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('technician_name', ''),
        data.get('employee_id', ''),
        data.get('date', ''),
        data.get('route_zone', ''),
        data.get('start_time', ''),
        data.get('end_time', ''),
        data.get('total_assigned', ''),
        data.get('meters_read', ''),
        data.get('no_access', ''),
        data.get('faulty_meters', ''),
        data.get('reports_filed', ''),
        data.get('document_type', ''),
        data.get('notes', ''),
        property_grid_json
    ))
    
    reading_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✓ Saved reading ID: {reading_id}")
    return reading_id

def get_all_readings():
    """Get all readings from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM readings ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    readings = []
    for row in rows:
        readings.append({
            'id': row[0],
            'technician_name': row[1],
            'employee_id': row[2],
            'date': row[3],
            'route_zone': row[4],
            'start_time': row[5],
            'end_time': row[6],
            'total_assigned': row[7],
            'meters_read': row[8],
            'no_access': row[9],
            'faulty_meters': row[10],
            'reports_filed': row[11],
            'document_type': row[12],
            'notes': row[13],
            'property_grid': json.loads(row[14]) if row[14] else [],
            'created_at': row[15]
        })
    
    conn.close()
    return readings

def get_reading_by_id(reading_id):
    """Get a single reading by ID"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM readings WHERE id = ?", (reading_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'technician_name': row[1],
            'employee_id': row[2],
            'date': row[3],
            'route_zone': row[4],
            'start_time': row[5],
            'end_time': row[6],
            'total_assigned': row[7],
            'meters_read': row[8],
            'no_access': row[9],
            'faulty_meters': row[10],
            'reports_filed': row[11],
            'document_type': row[12],
            'notes': row[13],
            'property_grid': json.loads(row[14]) if row[14] else [],
            'created_at': row[15]
        }
    return None

# Initialize database on import
init_database()