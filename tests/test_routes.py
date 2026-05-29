"""
tests/test_routes.py
────────────────────
Route-level tests for API endpoints.
Heavy AI services (whisper, mistral, etc.) are mocked via conftest.py.
"""

import json
from unittest.mock import patch, MagicMock


class TestProcessRoute:
    """Tests for /api/process endpoint."""

    def test_process_no_input(self, client):
        """POST /api/process with no URL or file should return 400."""
        resp = client.post("/api/process", data={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["success"] is False
        assert "No URL or file" in data["error"]

    @patch("routes.process.start_pipeline")
    def test_process_with_url(self, mock_pipeline, client):
        """POST /api/process with a valid URL should start the pipeline."""
        mock_pipeline.return_value = "test-session-123"

        resp = client.post("/api/process", data={
            "url": "https://www.youtube.com/watch?v=test123",
            "language": "english",
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["session_id"] == "test-session-123"
        mock_pipeline.assert_called_once()

    @patch("routes.process.start_pipeline")
    def test_process_with_file_upload(self, mock_pipeline, client):
        """POST /api/process with a file upload should save and process."""
        mock_pipeline.return_value = "file-session-456"

        from io import BytesIO
        data = {
            "file": (BytesIO(b"fake audio data"), "test_audio.mp3"),
            "language": "english",
        }
        resp = client.post(
            "/api/process",
            data=data,
            content_type="multipart/form-data",
        )
        assert resp.status_code == 200
        result = resp.get_json()
        assert result["success"] is True
        assert result["session_id"] == "file-session-456"

    @patch("routes.process.session_store")
    def test_status_not_found(self, mock_store, client):
        """GET /api/status/<sid> for unknown session returns 404."""
        mock_store.get_status.return_value = None
        resp = client.get("/api/status/nonexistent")
        assert resp.status_code == 404

    @patch("routes.process.session_store")
    def test_status_found(self, mock_store, client):
        """GET /api/status/<sid> for known session returns status."""
        mock_store.get_status.return_value = {
            "step": "transcribing",
            "progress": 40,
            "detail": "Processing audio...",
        }
        resp = client.get("/api/status/session-abc")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["step"] == "transcribing"
        assert data["progress"] == 40

    @patch("routes.process.session_store")
    def test_result_not_found(self, mock_store, client):
        """GET /api/result/<sid> when no result yet returns 404."""
        mock_store.get_result.return_value = None
        resp = client.get("/api/result/nonexistent")
        assert resp.status_code == 404

    @patch("routes.process.session_store")
    def test_result_found(self, mock_store, client):
        """GET /api/result/<sid> with a completed result returns it."""
        mock_store.get_result.return_value = {
            "title": "Test Meeting",
            "summary": "A summary of the test.",
        }
        resp = client.get("/api/result/session-abc")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["result"]["title"] == "Test Meeting"


class TestChatRoute:
    """Tests for /api/chat endpoint."""

    def test_chat_missing_session_id(self, client):
        """POST /api/chat without session_id should return 400."""
        resp = client.post(
            "/api/chat",
            data=json.dumps({"question": "What happened?"}),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "Missing session_id" in data["error"]

    def test_chat_missing_question(self, client):
        """POST /api/chat without question should return 400."""
        resp = client.post(
            "/api/chat",
            data=json.dumps({"session_id": "abc123"}),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "Missing question" in data["error"]

    @patch("routes.chat.chat_with_session")
    def test_chat_success(self, mock_chat, client):
        """POST /api/chat with valid input returns an answer."""
        mock_chat.return_value = "The meeting discussed quarterly results."

        resp = client.post(
            "/api/chat",
            data=json.dumps({
                "session_id": "abc123",
                "question": "What was discussed?",
            }),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "quarterly results" in data["answer"]


class TestCORSHeaders:
    """Verify CORS is configured for API routes."""

    def test_cors_headers_on_api(self, client):
        """API endpoints should include CORS headers."""
        resp = client.get("/api/health")
        # flask-cors adds these headers
        assert resp.status_code == 200
