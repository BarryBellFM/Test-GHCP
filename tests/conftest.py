"""
Test configuration and fixtures for the Mergington High School API tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to their initial state after each test"""
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team sport focusing on basketball skills and gameplay",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 16,
            "participants": ["sarah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["alex@mergington.edu", "taylor@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific concepts through experiments and projects",
            "schedule": "Thursdays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Express creativity through painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
        },
        "Theater Club": {
            "description": "Perform in school plays and develop acting skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(initial_state)
    
    yield
    
    # Reset again after test
    activities.clear()
    activities.update(initial_state)
