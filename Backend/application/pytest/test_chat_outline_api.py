import pytest
import requests

BASE_URL = "http://localhost:5000"  # Ensure your Flask app is running locally

# Helper function to login and get auth token
def login_and_get_token(username, password):
    response = requests.post(f"{BASE_URL}/user_login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200, f"Login failed for {username}: {response.text}"
    return response.json()["data"]["token"]

@pytest.fixture(scope="module")
def student_token():
    """Fixture to get an authentication token for a student."""
    return login_and_get_token("dummy_student", "password")

@pytest.fixture(scope="module")
def invalid_token():
    """Fixture to simulate an invalid authentication token."""
    return "invalid-token"

# Test cases for ChatOutline API

def test_fetch_chats_invalid_course_id(student_token):
    """Test fetching chats when course doesn't exist."""
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/chats/999", headers=headers)  # Invalid course ID
    
    assert response.status_code == 402, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "You have not enrolled to the course"

def test_fetch_chats_no_chats(student_token):
    """Test fetching chats when no chats exist."""
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/chats/1", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "No chats found"


def test_fetch_chats_invalid_auth(invalid_token):
    """Test fetching chats with an invalid authentication token."""
    headers = {"Authentication-Token": invalid_token}
    
    response = requests.get(f"{BASE_URL}/chats/1", headers=headers)
    
    assert response.status_code == 401, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]


def test_create_chat_success(student_token):
    """Test creating a new chat successfully."""
    headers = {"Authentication-Token": student_token}
    payload = {
        "query": "Tell me more about Python lists",
        "tag": "1-1-1"
    }
    
    response = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    
    assert response.status_code == 200, f"Failed to create chat: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    assert data["status"]["message"] == "Chat Created successfully"
    assert "session_id" in data["data"]

def test_fetch_chats_success(student_token):
    """Test fetching chats successfully."""
    headers = {"Authentication-Token": student_token}

    response = requests.get(f"{BASE_URL}/chats/1", headers=headers)

    assert response.status_code == 200, f"Failed to fetch chats: {response.text}"

    data = response.json()

    assert data["status"]["success"] in [1, True]
    assert isinstance(data["data"], list), "Expected data to be a list of chats"
    assert len(data["data"]) > 0, "No chats found"


def test_create_chat_missing_fields(student_token):
    """Test creating a chat with missing fields."""
    headers = {"Authentication-Token": student_token}
    
    # Missing 'query' field
    payload = {
        "tag": "1-1-1"
    }
    
    response = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    
    assert response.status_code == 403, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Missing input fields"


def test_create_chat_invalid_auth(invalid_token):
    """Test creating a chat with an invalid authentication token."""
    headers = {"Authentication-Token": invalid_token}
    
    payload = {
        "query": "Tell me more about Python lists",
        "tag": "1-1-1"
    }
    
    response = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    
    assert response.status_code == 401, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]
