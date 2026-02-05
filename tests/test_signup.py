"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_successful(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client, reset_activities):
    """Test that signup actually adds the participant to the activity"""
    # Get initial state
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Signup
    client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    
    # Verify participant was added
    response = client.get("/activities")
    final_count = len(response.json()["Chess Club"]["participants"])
    assert final_count == initial_count + 1
    assert "newstudent@mergington.edu" in response.json()["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email(client, reset_activities):
    """Test signup fails if student is already signed up"""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_different_activities(client, reset_activities):
    """Test that a student can sign up for multiple different activities"""
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup?email=newstudent@mergington.edu"
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    assert "newstudent@mergington.edu" in response.json()["Chess Club"]["participants"]
    assert "newstudent@mergington.edu" in response.json()["Programming Class"]["participants"]


def test_signup_special_characters_in_email(client, reset_activities):
    """Test signup with special characters in email"""
    email = "student+test@mergington.edu"
    # Use params dict for proper URL encoding of special characters
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    assert email in response.json()["message"]
