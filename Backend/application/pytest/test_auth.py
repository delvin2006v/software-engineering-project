import requests

BASE_URL = "http://localhost:5000"  # Ensure your Flask app is running on this URL

def test_login_success():
    """Test successful login."""
    response = requests.post(f"{BASE_URL}/user_login", json={
        "username": "dummy_student",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"]["success"] in [True, 1]
    assert "token" in data["data"]


def test_login_missing_username():
    """Test login with missing username."""
    response = requests.post(f"{BASE_URL}/user_login", json={
        "password": "password"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["status"]["message"] == "Missing input fields"


def test_login_invalid_username():
    """Test login with invalid username."""
    response = requests.post(f"{BASE_URL}/user_login", json={
        "username": "unknown_user",
        "password": "password"
    })
    assert response.status_code == 404
    data = response.json()
    assert "does not exists" in data["status"]["message"]


def test_login_incorrect_password():
    """Test login with incorrect password."""
    response = requests.post(f"{BASE_URL}/user_login", json={
        "username": "dummy_student",
        "password": "wrong_password"
    })
    assert response.status_code == 403
    data = response.json()
    assert data["status"]["message"] == "Incorrect Password"
