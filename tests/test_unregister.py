"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""

import pytest
import copy


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, sample_activities, monkeypatch):
        """
        Test: Student can successfully unregister from an activity.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities, use existing participant
        - Act: DELETE request to unregister student
        - Assert: Response 200, student removed from participants list
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"
        
        # Verify student is in the activity before unregistering
        assert student_email in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert student_email in data["message"]
        assert activity_name in data["message"]
        
        # Verify student was actually removed from participants
        import app
        assert student_email not in app.activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client, sample_activities, monkeypatch):
        """
        Test: Unregistering from non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities, use non-existent activity
        - Act: DELETE request to unregister from non-existent activity
        - Assert: Response 404 with appropriate error message
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        non_existent_activity = "Nonexistent Club"
        student_email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{non_existent_activity}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered(self, client, sample_activities, monkeypatch):
        """
        Test: Cannot unregister a student who is not registered.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities, use email not in participants
        - Act: DELETE request to unregister non-existent participant
        - Assert: Response 400 with appropriate error message
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Chess Club"
        unregistered_student = "nobody@mergington.edu"
        
        # Verify student is NOT in the activity
        assert unregistered_student not in sample_activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": unregistered_student}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower() or "Not registered" in data["detail"]

    def test_unregister_idempotent_error(self, client, sample_activities, monkeypatch):
        """
        Test: Unregistering twice returns error on second attempt.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities and existing participant
        - Act: First DELETE (success), second DELETE (failure)
        - Assert: First returns 200, second returns 400
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Art Studio"
        student_email = "ava@mergington.edu"
        
        # Verify student is in the activity
        assert student_email in sample_activities[activity_name]["participants"]
        
        # Act - First unregister (should succeed)
        response1 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Act - Second unregister (should fail)
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        
        # Verify student is gone
        import app
        assert student_email not in app.activities[activity_name]["participants"]

    def test_unregister_response_format(self, client, sample_activities, monkeypatch):
        """
        Test: Unregister response has proper message format.
        
        AAA Pattern:
        - Arrange: Set up test client with mocked activities
        - Act: DELETE request to unregister
        - Assert: Response has correct message structure
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Music Band"
        student_email = "noah@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert isinstance(data["message"], str)
        assert "Unregistered" in data["message"]
        assert student_email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_other_participants_unaffected(self, client, sample_activities, monkeypatch):
        """
        Test: Unregistering one student doesn't affect others in the same activity.
        
        AAA Pattern:
        - Arrange: Set up test client with activity that has multiple participants
        - Act: DELETE to unregister one student
        - Assert: Other participants remain in the activity
        """
        # Arrange
        monkeypatch.setattr("app.activities", copy.deepcopy(sample_activities))
        activity_name = "Chess Club"
        
        # Get the participants before
        participants_before = sample_activities[activity_name]["participants"].copy()
        assert len(participants_before) >= 2
        
        student_to_remove = participants_before[0]
        other_student = participants_before[1]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        
        import app
        participants_after = app.activities[activity_name]["participants"]
        
        # Verify removed student is gone
        assert student_to_remove not in participants_after
        
        # Verify other student is still there
        assert other_student in participants_after
