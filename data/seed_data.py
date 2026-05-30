import sys
import os

# Append the parent directory to the system path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_db_connection, init_db

def seed_database():
    print("Initializing Database...")
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clean previous data to prevent duplicates on multiple runs
    cursor.execute("DELETE FROM facilities")
    cursor.execute("DELETE FROM roadside_services")
    cursor.execute("DELETE FROM global_emergency_contacts")
    cursor.execute("DELETE FROM user_profile")
    
    print("Seeding Global Emergency Contacts...")
    contacts = [
        # Country, Code, National, Police, Ambulance, Fire, Trauma Hotline
        ('India', 'IN', '112', '100', '102', '101', '1099'),
        ('United States', 'US', '911', '911', '911', '911', '1-800-222-1222'),
        ('United Kingdom', 'GB', '999', '999', '999', '999', '111'),
        ('Australia', 'AU', '000', '000', '000', '000', '131126'),
        ('Germany', 'DE', '112', '110', '112', '112', '112')
    ]
    cursor.executemany("""
    INSERT INTO global_emergency_contacts (country_name, country_code, national_emergency, police, ambulance, fire, trauma_hotline)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, contacts)
    
    print("Seeding Facilities (Trauma Centers, Hospitals, Police, Ambulances)...")
    facilities = [
        # 1. NEW DELHI (lat: 28.6139, lon: 77.2090)
        ('AIIMS Trauma Centre', 'Trauma Center Level I', 28.5672, 77.2100, '+91 11 2659 3162', '+91 11 2658 8700', 'Ring Rd, Ansari Nagar, New Delhi', '24/7', 'ICU, Neuro, Ortho, Burn Care, Cardio', 'IN'),
        ('Safdarjung Hospital Emergency', 'Hospital', 28.5685, 77.2061, '+91 11 2673 0000', None, 'Ansari Nagar, Opp AIIMS, New Delhi', '24/7', 'General Triage, Trauma, ICU', 'IN'),
        ('Max Super Speciality Emergency', 'Hospital', 28.5284, 77.2201, '+91 11 2651 5050', '+91 11 4055 4055', 'Press Enclave Road, Saket, New Delhi', '24/7', 'Cardiology, Neurology, Emergency Trauma', 'IN'),
        ('Delhi Police Station - Connaught Place', 'Police', 28.6295, 77.2198, '+91 11 2334 1414', '100', 'Connaught Place, New Delhi', '24/7', 'Law Enforcement, Accident Dispatch', 'IN'),
        ('Fortis Flt. Lt. Rajan Dhall Hospital', 'Hospital', 28.5273, 77.1511, '+91 11 4277 6222', None, 'Sector B, Pocket 1, Vasant Kunj, New Delhi', '24/7', 'Multi-Specialty Emergency Care', 'IN'),
        ('Central Delhi EMS - Ambulance Station 1', 'Ambulance Station', 28.6105, 77.2215, '+91 99999 10201', '102', 'India Gate Area, New Delhi', '24/7', 'Advanced Life Support (ALS) Ambulances', 'IN'),
        ('South Delhi Emergency Dispatch', 'Ambulance Station', 28.5450, 77.1950, '+91 98888 10202', '102', 'Green Park, New Delhi', '24/7', 'Basic & Advanced Trauma Support Mobile Units', 'IN'),
        
        # 2. BENGALURU (lat: 12.9716, lon: 77.5946)
        ('NIMHANS Emergency Brain & Spine', 'Trauma Center Level I', 12.9431, 77.5971, '+91 80 2699 5000', '+91 80 2699 5200', 'Hosur Road, Wilson Garden, Bengaluru', '24/7', 'Neuro-trauma, Spine Injury, Critical ICU', 'IN'),
        ('St. John\'s Medical College Hospital', 'Trauma Center Level I', 12.9333, 77.6244, '+91 80 2206 5000', '+91 80 2206 5100', 'Sarjapur Road, John Nagar, Bengaluru', '24/7', 'Trauma Resuscitation, Cardiac, Surgery', 'IN'),
        ('Manipal Hospital Emergency Unit', 'Hospital', 12.9592, 77.6436, '+91 80 2502 4444', '+91 80 2526 6666', 'HAL Old Airport Rd, Kodihalli, Bengaluru', '24/7', 'Cardiac Response, Stroke, Emergency Surgery', 'IN'),
        ('Cubbon Park Police Station', 'Police', 12.9740, 77.5960, '+91 80 2294 2210', '100', 'Kasturba Road, Near Cubbon Park, Bengaluru', '24/7', 'Traffic Accidents Response, Patrol', 'IN'),
        ('Bengaluru Central Ambulance Dispatch', 'Ambulance Station', 12.9710, 77.5900, '+91 90000 10299', '102', 'M.G. Road Metro Complex, Bengaluru', '24/7', 'Cardiac & Trauma Response Fleet', 'IN'),
        ('Indiranagar Rescue Base', 'Ambulance Station', 12.9784, 77.6408, '+91 91111 10299', '102', '100 Feet Rd, Indiranagar, Bengaluru', '24/7', '2 ALS Rapid Ambulances', 'IN'),
        
        # 3. MUMBAI (lat: 19.0760, lon: 72.8777)
        ('KEM Hospital Triage Centre', 'Trauma Center Level I', 19.0026, 72.8421, '+91 22 2410 7000', None, 'Acharya Donde Marg, Parel, Mumbai', '24/7', 'General Triage, Trauma ICU, Pediatric Care', 'IN'),
        ('H. N. Reliance Foundation Hospital', 'Hospital', 18.9575, 72.8193, '+91 22 6130 3030', '+91 22 6130 3000', 'Raja Rammohan Roy Rd, Prarthana Samaj, Mumbai', '24/7', 'Comprehensive Stroke, Cardiac Triage', 'IN'),
        ('Bandrakurla Complex Police Base', 'Police', 19.0596, 72.8680, '+91 22 2650 4000', '100', 'BKC G-Block, Bandra East, Mumbai', '24/7', 'Accident Reports, BKC Flyover Dispatch', 'IN'),
        ('Mumbai North Ambulance Outpost', 'Ambulance Station', 19.1200, 72.8500, '+91 92222 10288', '102', 'Western Express Highway, Andheri, Mumbai', '24/7', 'Highway Incident Rapid Ambulances', 'IN'),
        
        # 4. NEW YORK CITY (lat: 40.7128, lon: -74.0060)
        ('Bellevue Hospital Trauma Center', 'Trauma Center Level I', 40.7388, -73.9744, '+1 212-562-4141', None, '462 1st Ave, New York, NY 10016', '24/7', 'Level 1 Trauma, Burn Unit, Psychiatric Triage', 'US'),
        ('NYU Langone Health Emergency', 'Hospital', 40.7424, -73.9740, '+1 212-263-5555', None, '550 1st Ave, New York, NY 10016', '24/7', 'Cardiac Center, Pediatric Emergency, Stroke Center', 'US'),
        ('NYPD 9th Precinct', 'Police', 40.7265, -73.9858, '+1 212-477-7811', '911', '321 E 5th St, New York, NY 10003', '24/7', 'Local Crime & Auto Accidents Response', 'US'),
        ('Manhattan South EMS Base', 'Ambulance Station', 40.7150, -74.0010, '+1 800-555-0199', '911', 'City Hall Park Area, New York, NY 10007', '24/7', 'FDNY Paramedics, Advanced Cardiac Units', 'US'),

        # 5. LONDON (lat: 51.5074, lon: -0.1278)
        ('Royal London Hospital Trauma', 'Trauma Center Level I', 51.5190, -0.0594, '+44 20 7377 7000', None, 'Whitechapel Rd, London E1 1FR', '24/7', 'Major Trauma Centre, Air Ambulance Base', 'GB'),
        ('St Thomas\' Hospital A&E', 'Hospital', 51.4988, -0.1190, '+44 20 7188 7188', None, 'Westminster Bridge Rd, London SE1 7EH', '24/7', 'Cardiac Resuscitation, Acute Pediatrics', 'GB'),
        ('Charing Cross Police Station', 'Police', 51.5085, -0.1265, '+44 20 7240 1212', '999', 'Agar St, London WC2N 4EA', '24/7', 'Metropolitan Police Incident Dispatch', 'GB'),
        ('Central London Ambulance Hub', 'Ambulance Station', 51.5050, -0.1300, '+44 20 8555 9999', '999', 'Westminster, London SW1A 0AA', '24/7', 'London Ambulance Service Rapid Responders', 'GB')
    ]
    cursor.executemany("""
    INSERT INTO facilities (name, type, latitude, longitude, contact_number, alt_contact_number, address, operating_hours, specialties, country_code)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, facilities)
    
    print("Seeding Roadside Support (Towing, Puncture Shops)...")
    services = [
        # 1. NEW DELHI
        ('Saket 24/7 Puncture Shop', 'Puncture Shop', 28.5255, 77.2185, '+91 97777 55501', 'Tube vulcanizing, tubeless repairs, nitrogen fill', 'IN'),
        ('Delhi Flatbed Towing Corp', 'Towing', 28.5550, 77.2350, '+91 98888 66601', 'Flatbed towing, wheel lift, dynamic recovery', 'IN'),
        ('Connaught Place Quick Puncture', 'Puncture Shop', 28.6310, 77.2210, '+91 95555 77701', 'Two-wheeler and four-wheeler express tyre repair', 'IN'),
        ('Vasant Kunj Towing Operators', 'Towing', 28.5190, 77.1620, '+91 91111 88801', 'Heavy vehicle towing, car lockouts, jumpstarts', 'IN'),
        
        # 2. BENGALURU
        ('Indiranagar Tyre & Puncture Care', 'Puncture Shop', 12.9720, 77.6415, '+91 98450 12345', 'Tubeless tyre puncture, wheel balancing, tyre patch', 'IN'),
        ('Namma Bengaluru Heavy Towing', 'Towing', 12.9550, 77.6250, '+91 98450 99999', '24hr Flatbed towing, accident recovery, pull-out service', 'IN'),
        ('Wilson Garden Puncture Outpost', 'Puncture Shop', 12.9410, 77.5920, '+91 99000 88811', 'Emergency motorcycle tube fix & car tyre patches', 'IN'),
        ('Koramangala Highway Roadside Assistance', 'Towing', 12.9300, 77.6350, '+91 97000 11122', 'Underlift towing, battery jumpstart, emergency fuel delivery', 'IN'),
        
        # 3. MUMBAI
        ('Parel Express Puncture & Tyre', 'Puncture Shop', 19.0010, 72.8450, '+91 91222 33344', 'Tubeless tyre repair, tyre replacement, air gauge', 'IN'),
        ('Bandra Highway Recovery Services', 'Towing', 19.0550, 72.8620, '+91 93222 44455', 'Flatbed towing, luxury car specialist recovery', 'IN'),
        
        # 4. NEW YORK
        ('Manhattan Mid-Town Puncture & Tire', 'Puncture Shop', 40.7410, -73.9800, '+1 212-555-0144', 'Tire patches, emergency rim replacement, wheel alignment', 'US'),
        ('Metro NYC Flatbed & Towing', 'Towing', 40.7300, -73.9700, '+1 212-555-0155', 'Standard towing, flatbed dispatch, accident removal', 'US'),
        
        # 5. LONDON
        ('Westminster Mobile Tyre Repair', 'Puncture Shop', 51.5030, -0.1250, '+44 20 7946 0122', 'Tyre vulcanisation, on-the-road emergency tyre swaps', 'GB'),
        ('Central London Heavy Towing Ltd', 'Towing', 51.5120, -0.0700, '+44 20 7946 0133', 'Accident recovery, vehicle relocation, low-clearance garages', 'GB')
    ]
    cursor.executemany("""
    INSERT INTO roadside_services (name, type, latitude, longitude, contact_number, services_offered, country_code)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, services)
    
    print("Seeding Active User Profile...")
    profile = {
        'full_name': 'Karan Malhotra',
        'blood_group': 'A+ Positive',
        'medical_allergies': 'Penicillin, Sulfa drugs',
        'chronic_conditions': 'Mild Asthma (uses inhaler)',
        'ice_contact_name_1': 'Aarti Malhotra (Wife)',
        'ice_contact_phone_1': '+91 99999 88888',
        'ice_contact_name_2': 'Dr. Rajesh Gupta (Family Doctor)',
        'ice_contact_phone_2': '+91 98888 77777'
    }
    cursor.execute("""
    INSERT INTO user_profile (full_name, blood_group, medical_allergies, chronic_conditions, ice_contact_name_1, ice_contact_phone_1, ice_contact_name_2, ice_contact_phone_2)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile['full_name'], profile['blood_group'], profile['medical_allergies'], profile['chronic_conditions'],
        profile['ice_contact_name_1'], profile['ice_contact_phone_1'], profile['ice_contact_name_2'], profile['ice_contact_phone_2']
    ))
    
    conn.commit()
    conn.close()
    print("Database seeding completed successfully! Total entries populated:")
    print(" - Contacts, facilities, roadside services, and profile set.")

if __name__ == "__main__":
    seed_database()
