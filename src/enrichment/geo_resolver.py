import requests
import time
from typing import Dict, Any, List
from src.utils.helpers import is_public_ip
from src.config.config_loader import ConfigLoader

class GeoResolver:
    """Resolves IP addresses to geographical locations using ip-api.com."""
    
    def __init__(self):
        config = ConfigLoader()
        self.base_url = config.get("geoip.base_url", "http://ip-api.com/json")
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = config.get("geoip.cache_ttl", 3600)
        self.last_request_time = 0.0
        self.min_interval = 60.0 / config.get("geoip.rate_limit", 45)
        
    def resolve(self, ip: str) -> Dict[str, Any]:
        """Resolves a single IP address."""
        if not is_public_ip(ip):
            return {"country": "Local Network", "city": "Local", "lat": 0.0, "lon": 0.0, "status": "fail"}
            
        now = time.time()
        
        # Check cache
        if ip in self.cache:
            entry = self.cache[ip]
            if now - entry['timestamp'] < self.cache_ttl:
                return entry['data']
                
        # Rate limiting
        time_since_last = now - self.last_request_time
        if time_since_last < self.min_interval:
            time.sleep(self.min_interval - time_since_last)
            
        try:
            self.last_request_time = time.time()
            response = requests.get(f"{self.base_url}/{ip}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result = {
                        "country": data.get("country", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "lat": data.get("lat", 0.0),
                        "lon": data.get("lon", 0.0),
                        "status": "success"
                    }
                else:
                    result = {"country": "Unknown", "city": "Unknown", "lat": 0.0, "lon": 0.0, "status": "fail"}
                    
                self.cache[ip] = {'timestamp': time.time(), 'data': result}
                return result
        except requests.RequestException:
            pass
            
        return {"country": "Unknown", "city": "Unknown", "lat": 0.0, "lon": 0.0, "status": "fail"}
        
    def resolve_batch(self, ips: List[str]) -> Dict[str, Dict[str, Any]]:
        """Resolves multiple IPs efficiently."""
        results = {}
        # Get unique IPs
        unique_ips = list(set(ips))
        for ip in unique_ips:
            results[ip] = self.resolve(ip)
        return results
