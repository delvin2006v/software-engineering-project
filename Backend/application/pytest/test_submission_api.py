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

# Test cases for Submission API

def test_create_submission_success(student_token):
    """Test successful submission creation."""
    headers = {"Authentication-Token": student_token}
    payload = {
        "assignment_id": "1-1-6",
        "content": "[{\"id\": 1, \"option\": [\"12\"]}]"
    }
    response = requests.post(f"{BASE_URL}/submissions", json=payload, headers=headers)
    
    assert response.status_code == 200, f"Failed to create submission: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] is True
    assert data["data"]["points"] > 0
    assert "content" in data["data"]


def test_create_submission_course_not_found(student_token):
    """Test submission creation with a non-existent course."""
    headers = {"Authentication-Token": student_token}
    payload = {
        "assignment_id": "999-1-6",  # Invalid course ID
        "content": "[{\"id\": 1, \"option\": [\"12\"]}]"
    }
    response = requests.post(f"{BASE_URL}/submissions", json=payload, headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Course not found"


def test_create_submission_assignment_not_found(student_token):
    """Test submission creation with a non-existent assignment."""
    headers = {"Authentication-Token": student_token}
    payload = {
        "assignment_id": "1-999-6",  # Invalid assignment ID
        "content": "[{\"id\": 1, \"option\": [\"12\"]}]"
    }
    response = requests.post(f"{BASE_URL}/submissions", json=payload, headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Assignment not found"


def test_create_submission_invalid_auth(invalid_token):
    """Test submission creation with an invalid authentication token."""
    headers = {"Authentication-Token": invalid_token}
    payload = {
        "assignment_id": "1-1-6",
        "content": "[{\"id\": 1, \"option\": [\"12\"]}]"
    }
    response = requests.post(f"{BASE_URL}/submissions", json=payload, headers=headers)
    
    assert response.status_code == 401, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]


def test_retrieve_submission_success(student_token):
    """Test retrieving the latest submission for a valid assignment ID."""
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/submissions/1-1-6", headers=headers)
    
    assert response.status_code == 200, f"Failed to retrieve submission: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1,True]
    assert "submission" in data["data"]
    assert data["data"]["submission"]["id"] > 0


def test_retrieve_submission_no_submissions_yet(student_token):
    """Test retrieving submissions when no submissions exist for the assignment."""
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/submissions/999-999-999", headers=headers)  # Assignment ID with no submissions
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "You haven't made any submission yet"


def test_retrieve_submission_invalid_auth(invalid_token):
    """Test retrieving submissions with an invalid authentication token."""
    headers = {"Authentication-Token": invalid_token}
    
    response = requests.get(f"{BASE_URL}/submissions/1-1-6", headers=headers)
    
    assert response.status_code == 401, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]
