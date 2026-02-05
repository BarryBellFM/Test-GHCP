"""
Tests for the GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Basketball" in data


def test_get_activities_contains_required_fields(client, reset_activities):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_participants_are_lists(client, reset_activities):
    """Test that participants are returned as lists"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list)


def test_get_activities_correct_participant_count(client, reset_activities):
    """Test that participant counts are correct"""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club should have 2 participants
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
