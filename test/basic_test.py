import requests

BASE_URL = "http://localhost:8000"

print("=== API Test ===")

try:
    # Health check
    url = BASE_URL + "/health"
    response = requests.get(url)
    print("Health:", response.status_code)
    
    # Get token
    url = BASE_URL + "/api/v1/token"
    data = {"appId": "com.funtriolimited.slots.casino.free"}
    response = requests.post(url, json=data)
    print("Token:", response.status_code)
    token = response.json().get("token") if response.status_code == 200 else None
    
    # Login
    url = BASE_URL + "/api/v1/login?loginType=1&loginId=test123"
    response = requests.get(url)
    print("Login:", response.status_code)
    
    # Daily gift
    url = BASE_URL + "/api/v1/daily_gift"
    data = {"uid": "test123"}
    response = requests.post(url, json=data)
    print("Daily gift:", response.status_code)
    
    # Store items
    url = BASE_URL + "/api/v1/store/items"
    data = {"uid": "test123"}
    response = requests.post(url, json=data)
    print("Store items:", response.status_code)
    
    # Payment success (if token available)
    if token:
        url = BASE_URL + "/api/v1/payment/success"
        headers = {"Authorization": "Bearer " + token}
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
        response = requests.post(url, json=data, headers=headers)
        print("Payment success:", response.status_code)
        
        # Payment failure
        url = BASE_URL + "/api/v1/payment/failure"
        data["web_pay_error_code"] = "card_declined"
        response = requests.post(url, json=data, headers=headers)
        print("Payment failure:", response.status_code)
    
    # Order history
    url = BASE_URL + "/api/v1/orders/history"
    data = {"uid": "test123"}
    response = requests.post(url, json=data)
    print("Order history:", response.status_code)
    
    print("Test completed!")
    
except Exception as e:
    print("Error:", e)