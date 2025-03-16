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

@pytest.fixture(scope="module")
def created_session_id(student_token):
    headers = {"Authentication-Token": student_token}
    payload = {
        "query": "Tell me more about python lists",
        "tag": "1-1-1"
    }
    response = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    assert response.status_code == 200, f"Chat creation failed: {response.text}"
    data = response.json()
    return data["data"]["session_id"]

# Test cases for Chat API

def test_fetch_chat_success(student_token, created_session_id):
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/chats/1/{created_session_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    assert "chat" in data["data"]
    assert len(data["data"]["chat"]) > 0



def test_fetch_chat_not_found(student_token):
    """Test fetching a non-existent chat."""
    headers = {"Authentication-Token": student_token}

    # Fetch chat with invalid session_id
    response = requests.get(f"{BASE_URL}/chats/1/999", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Chat history not found"


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
    assert data["data"]["message"]["role"] == "agent"
    assert "session_id" in data["data"]


def test_create_chat_missing_fields(student_token):
    """Test creating a new chat with missing fields."""
    headers = {"Authentication-Token": student_token}
    payload = {
        "query": "Tell me more about Python lists"
        # Missing 'tag'
    }
    
    response = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    
    assert response.status_code == 403, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Missing input fields"


def test_add_message_to_chat_success(student_token,created_session_id):
    """Test adding a message to an existing chat successfully."""
    headers = {"Authentication-Token": student_token}
    
    payload = {
        "query": "What is the difference between Python lists and tuples?",
        "tag": "1-1-2"
    }
    
    # Add message to chat with course_id=1 and session_id=0
    response = requests.post(f"{BASE_URL}/chats/1/{created_session_id}", json=payload, headers=headers)
    
    assert response.status_code == 200, f"Failed to add message: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    assert data["data"]["message"]["role"] == "agent"


def test_add_message_to_non_existent_chat(student_token):
    """Test adding a message to a non-existent chat."""
    headers = {"Authentication-Token": student_token}
    
    payload = {
        "query": "What is the difference between Python lists and tuples?",
        "tag": "1-1-2"
    }
    
    # Add message to a non-existent chat
    response = requests.post(f"{BASE_URL}/chats/1/999", json=payload, headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Chat history not found"


def test_delete_chat_success(student_token, created_session_id):
    headers = {"Authentication-Token": student_token}

    response = requests.delete(f"{BASE_URL}/chats/1/{created_session_id}", headers=headers)
    
    assert response.status_code == 200, f"Failed to delete chat: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    

def test_delete_non_existent_chat(student_token):
    """Test deleting a non-existent chat."""
    headers = {"Authentication-Token": student_token}

    # Attempt to delete a non-existent chat
    response = requests.delete(f"{BASE_URL}/chats/1/999", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Chat history not found"


def test_export_chat_success(student_token):
    """Test exporting an existing chat successfully."""
    headers = {"Authentication-Token": student_token}

    # Create a new chat first
    payload = {
        "query": "Tell me more about Python lists",
        "tag": "1-1-1"
    }
    response_create = requests.post(f"{BASE_URL}/chats/1", json=payload, headers=headers)
    assert response_create.status_code == 200, f"Failed to create chat: {response_create.text}"
    
    created_session_id = response_create.json()["data"]["session_id"]

    # Export the newly created chat
    response_export = requests.put(f"{BASE_URL}/chats/1/{created_session_id}", headers=headers)
    
    assert response_export.status_code == 200, f"Failed to export chat: {response_export.text}"
    
    data = response_export.json()
    
    assert data["status"]["success"] in [1, True]
    assert "path" in data["data"]
