"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest
import copy


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_activities, new_student_email, monkeypatch):
        """
        Test: Student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Set up test client, mock activities, and new student email
        - Act: POST request to sign up student for activity
        - Assert: Response 200, student added to participants list
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_student_email in data["message"]
        assert activity_name in data["message"]
        
        # Verify student was actually added to participants
        import app
        assert new_student_email in app.activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client, sample_activities, new_student_email, monkeypatch):
        """
        Test: Signing up for non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities, use non-existent activity name
        - Act: POST request to sign up for non-existent activity
        - Assert: Response 404 with appropriate error message
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        non_existent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": new_student_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, client, sample_activities, monkeypatch):
        """
        Test: Student cannot sign up twice for the same activity.
        
        AAA Pattern:
        - Arrange: Set up test client, mocked activities with existing student
        - Act: POST request to sign up with email already in participants
        - Assert: Response 400 with appropriate error message
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Chess Club"
        
        # Use an email already in the activity
        existing_student = "michael@mergington.edu"
        assert existing_student in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_student}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower() or "Already signed up" in data["detail"]

    def test_signup_multiple_activities(self, client, sample_activities, new_student_email, monkeypatch):
        """
        Test: Student can sign up for multiple different activities.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities and new student
        - Act: POST requests to sign up for two different activities
        - Assert: Both signups succeed (200), student in both activities
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": new_student_email}
        )
        
        # Act - Second signup
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": new_student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        import app
        assert new_student_email in app.activities[activity1]["participants"]
        assert new_student_email in app.activities[activity2]["participants"]

    def test_signup_response_format(self, client, sample_activities, new_student_email, monkeypatch):
        """
        Test: Signup response has proper message format.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities
        - Act: POST request to sign up
        - Assert: Response has correct message structure
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Tennis Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert isinstance(data["message"], str)
        assert "Signed up" in data["message"]
        assert new_student_email in data["message"]
        assert activity_name in data["message"]
