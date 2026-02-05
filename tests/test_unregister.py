"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint
"""
import pytest


def test_unregister_successful(client, reset_activities):
    """Test successful unregistration from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregister actually removes the participant from the activity"""
    # Get initial state
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Unregister
    client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")
    
    # Verify participant was removed
    response = client.get("/activities")
    final_count = len(response.json()["Chess Club"]["participants"])
    assert final_count == initial_count - 1
    assert "michael@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregister from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_non_registered_participant(client, reset_activities):
    """Test unregister fails if student is not registered for the activity"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
    )
    
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_then_signup_again(client, reset_activities):
    """Test that a student can sign up again after unregistering"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Unregister
    response1 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response1.status_code == 200
    
    # Verify unregistered
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]
    
    # Sign up again
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify re-registered
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_unregister_all_participants(client, reset_activities):
    """Test unregistering all participants from an activity"""
    activity = "Tennis Club"
    
    # Get all participants
    response = client.get("/activities")
    participants = response.json()[activity]["participants"].copy()
    
    # Unregister all
    for email in participants:
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
    
    # Verify all are gone
    response = client.get("/activities")
    assert len(response.json()[activity]["participants"]) == 0
