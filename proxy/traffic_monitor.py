from mitmproxy import http
import requests
import time
import json
from datetime import datetime

# Backend URLs
BACKEND_URL = "http://localhost:5000/api/log-event"
ML_PREDICT_URL = "http://localhost:5001/predict"  # Python backend for ML

def request(flow: http.HTTPFlow):
    """Capture HTTP traffic and send to Node.js backend"""
    try:
        client_ip = flow.client_conn.address[0]
        url = flow.request.pretty_url
        method = flow.request.method
        host = flow.request.host
        path = flow.request.path
        payload_size = len(flow.request.raw_content) if flow.request.raw_content else 0
        timestamp = time.time()
        login_hour = datetime.fromtimestamp(timestamp).hour
        
        # Prepare data for backend
        log_data = {
            "client_ip": client_ip,
            "method": method,
            "host": host,
            "path": path,
            "url": url,
            "payload_size": payload_size,
            "timestamp": timestamp,
            "login_hour": login_hour,
            "files_accessed": 1,  # Each request counts
            "cpu_usage": 0,  # Can't get from network
            "network_packets": payload_size // 100,
            "source": "mitm_proxy",
            "is_anomaly": False  # Will be updated by backend
        }
        
        # Try to get ML prediction from Python backend
        try:
            ml_response = requests.post(
                ML_PREDICT_URL, 
                json={
                    "login_hour": login_hour,
                    "files_accessed": 1,
                    "cpu_usage": 0,
                    "network_packets": payload_size // 100
                },
                timeout=0.5
            )
            if ml_response.status_code == 200:
                log_data["is_anomaly"] = ml_response.json().get("anomaly", False)
        except:
            pass  # Python backend not running
        
        # Send to Node.js backend
        requests.post(BACKEND_URL, json=log_data, timeout=1)
        
        # Print status
        status = "⚠️ ANOMALY" if log_data["is_anomaly"] else "✅ Normal"
        print(f"[MITM] {status} - {method} {host}{path[:50]}")
        
    except Exception as e:
        print(f"[MITM Error] {e}")

def response(flow: http.HTTPFlow):
    """Also capture responses if needed"""
    pass