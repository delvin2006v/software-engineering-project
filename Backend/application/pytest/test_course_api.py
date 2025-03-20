import pytest
import requests
from helpers import login_and_get_token

BASE_URL = "http://localhost:5000"  # Ensure your Flask app is running locally

@pytest.fixture(scope="module")
def student_token():
    """Fixture to get an authentication token for a student."""
    return login_and_get_token("dummy_student", "password")

@pytest.fixture(scope="module")
def ta_token():
    """Fixture to get an authentication token for a TA."""
    return login_and_get_token("dummy_ta", "password")

@pytest.fixture(scope="module")
def instructor_token():
    """Fixture to get an authentication token for an instructor."""
    return login_and_get_token("dummy_instructor", "password")

@pytest.fixture(scope="module")
def auth_token():
    """Fixture to get an authentication token for a dummy user."""
    return login_and_get_token("dummy_student", "password")

@pytest.fixture(scope="module")
def no_enrollment():
    """Fixture to get an authentication token for a non-enrolled user."""
    return login_and_get_token('no-enrollment', 'password')

@pytest.fixture(scope="module")
def unauthenticated_headers():
    """Headers without any authentication token."""
    return {}

# Test cases

def test_fetch_all_courses_success(auth_token):
    """Test fetching all enrolled courses."""
    headers = {"Authentication-Token": auth_token}
    
    response = requests.get(f"{BASE_URL}/courses", headers=headers)
    
    assert response.status_code == 200, f"Failed to fetch courses: {response.text}"
    
    data = response.json()
    
    assert len(data["data"]["courses"]) > 0, f"No courses found: {data}"


def test_fetch_specific_course(auth_token):
    """Test fetching a specific course by ID."""
    headers = {"Authentication-Token": auth_token}
    
    response = requests.get(f"{BASE_URL}/courses/1", headers=headers)
    
    assert response.status_code == 200, f"Failed to fetch course: {response.text}"
    
    data = response.json()
    
    assert data["data"]["course"]["id"] == 1

def test_no_course_enrollment(no_enrollment):
    """Test fetching all enrolled courses."""
    headers = {"Authentication-Token": no_enrollment}
    
    response = requests.get(f"{BASE_URL}/courses", headers=headers)
    
    assert response.status_code == 404, f"No enrollment must fail"
    
    data = response.json()
    
    assert data['status']['message'] == 'You have not enrolled to any course'

def test_fetch_course_not_enrolled(auth_token):
    """Test fetching a course that the user is not enrolled in."""
    headers = {"Authentication-Token": auth_token}
    
    response = requests.get(f"{BASE_URL}/courses/2", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert data["status"]["message"] == "You have not enrolled to the course with id 2"


def test_fetch_invalid_course_id(auth_token):
    """Test fetching a course with an invalid ID."""
    headers = {"Authentication-Token": auth_token}
    
    response = requests.get(f"{BASE_URL}/courses/999", headers=headers)
    
    assert response.status_code == 404, f"Unexpected status code: {response.text}"
    
    data = response.json()
    
    assert "not enrolled" in data["status"]["message"]


def test_fetch_course_as_student(student_token):
    """Test fetching a specific course as a student."""
    headers = {"Authentication-Token": student_token}
    
    response = requests.get(f"{BASE_URL}/courses/1", headers=headers)
    
    assert response.status_code == 200, f"Failed to fetch course as student: {response.text}"
    
    data = response.json()
    
    assert data["data"]["course"]["id"] == 1
    assert data["data"]["course"]["name"] == "Programming in Python"  # Example course name


def test_fetch_course_as_ta(ta_token):
    """Test fetching a specific course as a TA."""
    headers = {"Authentication-Token": ta_token}
    
    response = requests.get(f"{BASE_URL}/courses/1", headers=headers)
    
    assert response.status_code == 402, "TA should not have access to this course"
    
    data = response.json()
    
    assert data["status"]["message"] == "You are not allowed to access that resource"


def test_fetch_course_as_instructor(instructor_token):
    """Test fetching a specific course as an instructor."""
    headers = {"Authentication-Token": instructor_token}
    
    response = requests.get(f"{BASE_URL}/courses/1", headers=headers)
    
    assert response.status_code == 402, "Instructor should not have access to this course"
    
    data = response.json()
    
    assert data["status"]["message"] == "You are not allowed to access that resource"


def test_unauthorized_access_to_course(unauthenticated_headers):
    """Test unauthorized access to a course without authentication."""
    response = requests.get(f"{BASE_URL}/courses/1", headers=unauthenticated_headers)
    
    assert response.status_code == 401, "Unauthorized request should fail"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]

def test_fetch_all_courses_failure(unauthenticated_headers):
    """Test unauthorized access to fetch all courses"""
    response = requests.get(f"{BASE_URL}/courses", headers=unauthenticated_headers)
    
    assert response.status_code == 401, "Unauthorized request should fail"
    
    data = response.json()
    
    assert data["status"]["message"] in ["Authentication Failed", "Invalid Authentication-Token provided"]