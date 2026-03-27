"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """
        Test: GET /activities returns all activities with 200 status.
        
        AAA Pattern:
        - Arrange: TestClient is ready (via fixture)
        - Act: GET request to /activities
        - Assert: Response 200 with activities dict containing expected keys
        """
        # Arrange (implicit via client fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is a dict (like the activities database)
        assert isinstance(data, dict)
        
        # Verify expected activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Team",
            "Science Club"
        ]
        
        for activity in expected_activities:
            assert activity in data

    def test_activities_have_required_fields(self, client):
        """
        Test: Each activity has required fields (description, schedule, max_participants, participants).
        
        AAA Pattern:
        - Arrange: TestClient is ready (via fixture)
        - Act: GET request to /activities
        - Assert: Each activity has all required fields
        """
        # Arrange (implicit via client fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str), f"Activity name should be string: {activity_name}"
            assert isinstance(activity_data, dict), f"Activity data should be dict: {activity_name}"
            
            # Check all required fields exist
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
            
            # Verify field types
            assert isinstance(activity_data["description"], str), f"Description should be string for {activity_name}"
            assert isinstance(activity_data["schedule"], str), f"Schedule should be string for {activity_name}"
            assert isinstance(activity_data["max_participants"], int), f"Max participants should be int for {activity_name}"
            assert isinstance(activity_data["participants"], list), f"Participants should be list for {activity_name}"

    def test_activities_participants_are_strings(self, client):
        """
        Test: All participant entries are email strings.
        
        AAA Pattern:
        - Arrange: TestClient is ready (via fixture)
        - Act: GET request to /activities
        - Assert: All participants are valid email strings
        """
        # Arrange (implicit via client fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), f"Participant should be string in {activity_name}"
                assert "@" in participant, f"Participant should be email format in {activity_name}: {participant}"
