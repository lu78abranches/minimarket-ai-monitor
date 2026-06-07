#!/usr/bin/env python3
"""
Test script to send sample events to the backend API
This verifies the backend persistence is working
"""

import requests
import time
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://minimarket-ai-monitor.onrender.com/api/events")

def send_test_events():
    """Send sample events to test the backend"""
    
    events = [
        {"personId": "person_001", "action": "ENTER", "location": "MAIN_ENTRANCE"},
        {"personId": "person_001", "action": "FRIDGE_INTERACTION", "location": "GELADEIRA_ESQUERDA"},
        {"personId": "person_001", "action": "FRIDGE_INTERACTION", "location": "GELADEIRA_DIREITA"},
        {"personId": "person_001", "action": "EXIT", "location": "MAIN_ENTRANCE"},
    ]
    
    print(f"Sending test events to: {BACKEND_URL}")
    print("=" * 50)
    
    for event in events:
        try:
            response = requests.post(BACKEND_URL, json=event, timeout=5)
            status = "✓ SUCCESS" if response.status_code == 201 else f"✗ FAILED ({response.status_code})"
            print(f"{status} | {event['action']:20} | person={event['personId']}")
            time.sleep(1)
        except Exception as e:
            print(f"✗ ERROR | {event['action']:20} | {str(e)}")
    
    print("=" * 50)
    print("Test completed! Check backend logs for event persistence.")

if __name__ == "__main__":
    send_test_events()
