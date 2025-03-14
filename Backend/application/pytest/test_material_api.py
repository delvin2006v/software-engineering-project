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
def instructor_token():
    """Fixture to get an authentication token for an instructor."""
    return login_and_get_token("dummy_instructor", "password")

@pytest.fixture(scope="module")
def ta_token():
    """Fixture to get an authentication token for a TA."""
    return login_and_get_token("dummy_ta", "password")

@pytest.fixture(scope="module")
def invalid_token():
    """Fixture to simulate an invalid authentication token."""
    return "invalid-token"

# Test cases for Material API

def test_fetch_materials_success(instructor_token):
    """Test fetching materials successfully."""
    headers = {"Authentication-Token": instructor_token}
    
    response = requests.get(f"{BASE_URL}/courses/1/materials", headers=headers)
    
    assert response.status_code == 200, f"Failed to fetch materials: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    assert "materials" in data["data"]


def test_fetch_materials_no_enrollment(ta_token):
    """Test fetching materials without enrollment."""
    headers = {"Authentication-Token": ta_token}
    
    response = requests.get(f"{BASE_URL}/courses/999/materials", headers=headers)  # Invalid course ID
    
    assert response.status_code == 402, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "You have not enrolled to the course"


def test_upload_material_success(instructor_token):
    """Test successful material upload."""
    headers = {"Authentication-Token": instructor_token}
    files = {
        "file": ("Example_Material.pdf", b"%PDF-1.4 Test PDF content."),
        "title": (None, "Example Material"),
        "type": (None, "pdf")
    }
    
    response = requests.post(f"{BASE_URL}/courses/1/materials", files=files, headers=headers)
    
    assert response.status_code == 200, f"Failed to upload material: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1, True]
    assert data["status"]["message"] == "Material uploaded successfully"



def test_edit_material_success(instructor_token):
    """Test editing an existing material."""
    headers = {"Authentication-Token": instructor_token}
    
    files = {
        "id": (None, 2),  # Existing material ID
        "file": ("updated_example.pdf", b"%PDF-1.4 Updated PDF content."),
        "title": (None, "Updated Example Material"),
        "type": (None, "pdf")
    }
    
    response = requests.put(f"{BASE_URL}/courses/1/materials", files=files, headers=headers)
    
    assert response.status_code == 200, f"Failed to edit material: {response.text}"
    
    data = response.json()
    
    assert data["status"]["success"] in [1,True]
    assert data["status"]["message"] == "Material edited successfully"


def test_edit_non_existent_material(instructor_token):
    """Test editing a non-existent material."""
    headers = {"Authentication-Token": instructor_token}
    
    files = {
        "id": (None, 999),  # Non-existent material ID
        "file": ("updated_file.pdf", b"%PDF-1.4 Updated PDF content."),
        "title": (None, "Updated File"),
        "type": (None, "pdf")
    }
    
    response = requests.put(f"{BASE_URL}/courses/1/materials", files=files, headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Material not found"


def test_delete_material_success(instructor_token):
    """Test deleting a material successfully."""
    headers = {"Authentication-Token": instructor_token}
    
    # Delete a material with ID 1
    response = requests.delete(f"{BASE_URL}/courses/1/materials/2", headers=headers)
    
    assert response.status_code == 200, f"Failed to delete material: {response.text}"


def test_delete_non_existent_material(instructor_token):
    """Test deleting a non-existent material."""
    headers = {"Authentication-Token": instructor_token}
    
    # Attempt to delete a non-existent material with ID 999
    response = requests.delete(f"{BASE_URL}/courses/1/materials/999", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "Material not found"
