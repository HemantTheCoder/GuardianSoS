import math
import requests

def get_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing (compass angle) from point 1 to point 2.
    Returns degrees (0-360).
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    return (bearing + 360) % 360

def bearing_to_direction(bearing):
    """
    Converts bearing angle into a compass direction string and unicode arrow indicator.
    """
    directions = [
        ("N", "↑", 0), ("NE", "↗", 45), ("E", "→", 90), ("SE", "↘", 135),
        ("S", "↓", 180), ("SW", "↙", 225), ("W", "←", 270), ("NW", "↖", 315)
    ]
    # Find closest direction
    idx = int((bearing + 22.5) / 45) % 8
    return directions[idx][0], directions[idx][1]

def geocode_online(address):
    """
    Attempts to geocode an address using the free, open Nominatim OpenStreetMap API.
    Returns (latitude, longitude, display_name) or None.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        headers = {"User-Agent": "GuardianSOS-Emergency-App-Hackathon"}
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                name = data[0]["display_name"]
                return lat, lon, name
    except Exception:
        pass
    return None

def reverse_geocode_online(lat, lon):
    """
    Attempts to reverse geocode coordinates to an address using OpenStreetMap.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        headers = {"User-Agent": "GuardianSOS-Emergency-App-Hackathon"}
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Unknown Location")
    except Exception:
        pass
    return "Unknown Address (Offline Mode)"

def get_ip_geolocation():
    """
    Attempts to fetch the user's current coordinates using their public IP.
    Extremely fast, zero permissions or user prompts required.
    """
    try:
        response = requests.get("http://ip-api.com/json", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "lat": float(data.get("lat")),
                    "lon": float(data.get("lon")),
                    "country": data.get("countryCode", "IN"),
                    "city": data.get("city", "Your Location")
                }
    except Exception:
        pass
    return None

