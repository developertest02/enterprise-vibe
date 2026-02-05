"""
Test script to demonstrate the user registration functionality
This would normally be in a tests/ directory, but placed here for demonstration purposes
"""

import requests
import json

# Example of how to test the registration endpoint
def test_registration():
    url = "http://localhost:5000/register"
    
    # Sample registration data
    registration_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123",
        "first_name": "Test",
        "last_name": "User",
        "display_name": "Test User"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, data=json.dumps(registration_data), headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response

if __name__ == "__main__":
    test_registration()