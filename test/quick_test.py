#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

BASE_URL = "http://localhost:8000"

def main():
    print("=== API Test ===")
    
    # Health check
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health: {response.status_code}")
    
    # Get token
    data = {"appId": "com.funtriolimited.slots.casino.free"}
    response = requests.post(f"{BASE_URL}/api/v1/token", json=data)
    print(f"Token: {response.status_code}")
    token = response.json().get("token") if response.status_code == 200 else None
    
    # Login
    response = requests.get(f"{BASE_URL}/api/v1/login?login_type=1&login_id=test123")
    print(f"Login: {response.status_code}")
    
    # Daily gift
    response = requests.post(f"{BASE_URL}/api/v1/daily_gift", json={"uid": "test123"})
    print(f"Daily gift: {response.status_code}")
    
    # Store items
    response = requests.post(f"{BASE_URL}/api/v1/store/items", json={"uid": "test123"})
    print(f"Store items: {response.status_code}")
    
    # Payment success (if token available)
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "order_id": "test_001",
            "uid": "test123",
            "item_id": 1,
            "price": 19.99,
            "currency": "USD",
            "payment_channel": "stripe",
            "payment_method": "card",
            "ip": "127.0.0.1",
            "country": "US",
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/api/v1/payment/success", json=data, headers=headers)
        print(f"Payment success: {response.status_code}")
        
        # Payment failure
        data["web_pay_error_code"] = "card_declined"
        response = requests.post(f"{BASE_URL}/api/v1/payment/failure", json=data, headers=headers)
        print(f"Payment failure: {response.status_code}")
    
    # Order history
    response = requests.post(f"{BASE_URL}/api/v1/orders/history", json={"uid": "test123"})
    print(f"Order history: {response.status_code}")
    
    print("Test completed!")

if __name__ == "__main__":
    main()