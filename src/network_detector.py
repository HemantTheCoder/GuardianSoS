import socket
import urllib.request

def check_actual_internet(timeout=1.5):
    """
    Checks if the system has an active internet connection by attempting
    to connect to a reliable DNS server or host.
    """
    try:
        # Check Cloudflare DNS (fastest)
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("1.1.1.1", 53))
        return True
    except (socket.error, Exception):
        try:
            # Fallback to HTTP request
            urllib.request.urlopen("https://www.google.com", timeout=timeout)
            return True
        except Exception:
            return False

def get_network_status(demo_override=None):
    """
    Determines the network health.
    Supports a demo override ('online', 'weak', 'offline').
    
    Returns:
        tuple: (status_string, explanation_string, badge_class)
    """
    if demo_override:
        status = demo_override.lower()
        if status == "offline":
            return "OFFLINE", "Decentralized SQLite Core Active (No Internet)", "badge-yellow"
        elif status == "weak":
            return "WEAK NETWORK", "Compressed Payload Mode Activated", "badge-yellow"
        else:
            return "ONLINE", "Cloud AI & Live Mapping Engaged", "badge-green"
            
    # If no override, check actual network status
    is_online = check_actual_internet()
    if is_online:
        return "ONLINE", "Cloud AI & Live Mapping Engaged", "badge-green"
    else:
        return "OFFLINE", "Decentralized SQLite Core Active (No Internet)", "badge-yellow"
