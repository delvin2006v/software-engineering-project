import requests

BASE_URL = "http://localhost:5000"

# login
def login_and_get_token(username, password):
    response = requests.post(f"{BASE_URL}/user_login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200, f"Login failed for {username}: {response.text}"
    return response.json()["data"]["token"]

# logout
def logout(token):
    response = requests.post(f"{BASE_URL}/user_logout", 
        headers={
        'Authentication-Token':token
    })
    assert response.status_code == 200, f"Logout failed : {response.text}"
    return True