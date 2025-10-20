import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


def test_root_redirect(client):
    """Test that root endpoint redirects to index.html"""
    response = client.get("/")
    assert response.status_code == 200  # FastAPI's RedirectResponse with automatic following
    # Note: TestClient automatically follows redirects


def test_get_activities(client):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert len(response.json()) > 0


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify the student was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonExistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate(client):
    """Test signing up for an activity twice"""
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    
    # First signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Try to signup again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity(client):
    """Test unregistering from an activity"""
    activity_name = "Chess Club"
    email = "unregister@mergington.edu"
    
    # First sign up
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify the student was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering when not registered"""
    response = client.post("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"