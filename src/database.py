import sqlite3
import math
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "guardiansos.db")

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on the Earth's surface
    using the Haversine formula. Returns distance in kilometers.
    """
    if None in (lat1, lon1, lat2, lon2):
        return 999999.0
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0 # Radius of earth in kilometers. Use 3956 for miles.
    return c * r

def get_db_connection():
    """
    Creates a connection to the SQLite database and registers the spatial Haversine function.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Register our custom spatial function in SQLite
    conn.create_function("HAVERSINE", 4, haversine_distance)
    return conn

def init_db():
    """
    Initializes the database schema if it doesn't already exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Emergency Facilities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        contact_number TEXT NOT NULL,
        alt_contact_number TEXT,
        address TEXT,
        operating_hours TEXT DEFAULT '24/7',
        specialties TEXT,
        country_code TEXT DEFAULT 'IN'
    )
    """)
    
    # 2. Roadside Support Services
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadside_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        contact_number TEXT NOT NULL,
        services_offered TEXT,
        country_code TEXT DEFAULT 'IN'
    )
    """)
    
    # 3. Global Emergency Contacts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS global_emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_name TEXT NOT NULL,
        country_code TEXT UNIQUE NOT NULL,
        national_emergency TEXT NOT NULL,
        police TEXT NOT NULL,
        ambulance TEXT NOT NULL,
        fire TEXT NOT NULL,
        trauma_hotline TEXT
    )
    """)
    
    # 4. User Profile & Medical Info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        medical_allergies TEXT,
        chronic_conditions TEXT,
        ice_contact_name_1 TEXT NOT NULL,
        ice_contact_phone_1 TEXT NOT NULL,
        ice_contact_name_2 TEXT,
        ice_contact_phone_2 TEXT
    )
    """)
    
    # 5. Incident Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        severity_level TEXT,
        accident_details TEXT,
        dispatched_facility_id INTEGER,
        offline_flag INTEGER DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()

def get_nearest_facilities(lat, lon, limit=5, facility_type=None):
    """
    Returns the nearest emergency facilities ordered by distance using spatial SQL query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if facility_type:
        query = """
        SELECT *, HAVERSINE(latitude, longitude, ?, ?) AS distance
        FROM facilities
        WHERE type = ?
        ORDER BY distance ASC
        LIMIT ?
        """
        cursor.execute(query, (lat, lon, facility_type, limit))
    else:
        query = """
        SELECT *, HAVERSINE(latitude, longitude, ?, ?) AS distance
        FROM facilities
        ORDER BY distance ASC
        LIMIT ?
        """
        cursor.execute(query, (lat, lon, limit))
        
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_nearest_roadside_services(lat, lon, limit=5, service_type=None):
    """
    Returns the nearest roadside support services ordered by distance using spatial SQL query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if service_type:
        query = """
        SELECT *, HAVERSINE(latitude, longitude, ?, ?) AS distance
        FROM roadside_services
        WHERE type = ?
        ORDER BY distance ASC
        LIMIT ?
        """
        cursor.execute(query, (lat, lon, service_type, limit))
    else:
        query = """
        SELECT *, HAVERSINE(latitude, longitude, ?, ?) AS distance
        FROM roadside_services
        ORDER BY distance ASC
        LIMIT ?
        """
        cursor.execute(query, (lat, lon, limit))
        
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_global_contact(country_code):
    """
    Returns the general emergency hotlines for a specific country.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM global_emergency_contacts WHERE country_code = ?", (country_code.upper(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_profile():
    """
    Returns the active user profile (if one exists).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_user_profile(profile_data):
    """
    Saves or updates the user medical profile.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clean previous profile for hackathon simplicity
    cursor.execute("DELETE FROM user_profile")
    
    query = """
    INSERT INTO user_profile (
        full_name, blood_group, medical_allergies, chronic_conditions,
        ice_contact_name_1, ice_contact_phone_1, ice_contact_name_2, ice_contact_phone_2
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        profile_data.get('full_name', 'Default User'),
        profile_data.get('blood_group', 'O+'),
        profile_data.get('medical_allergies', ''),
        profile_data.get('chronic_conditions', ''),
        profile_data.get('ice_contact_name_1', 'Emergency Contact'),
        profile_data.get('ice_contact_phone_1', '112'),
        profile_data.get('ice_contact_name_2', ''),
        profile_data.get('ice_contact_phone_2', '')
    ))
    conn.commit()
    conn.close()

def log_incident(lat, lon, severity, details, facility_id=None, offline=0):
    """
    Records an accident event, generating a legal dispatch log.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO emergency_logs (latitude, longitude, severity_level, accident_details, dispatched_facility_id, offline_flag)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (lat, lon, severity, details, facility_id, offline))
    conn.commit()
    conn.close()
