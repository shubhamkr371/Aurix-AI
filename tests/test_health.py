"""
tests/test_health.py
────────────────────
Smoke tests for the Flask app and health endpoint.
"""


def test_app_creates_successfully(app):
    """The Flask application factory should return an app instance."""
    assert app is not None


def test_health_endpoint(client):
    """GET /api/health should return 200 with status 'ok'."""
    resp = client.get("/api/health")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["status"] == "ok"
    assert "server" in data


def test_index_page(client):
    """GET / should serve the landing page HTML."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"html" in resp.data.lower() or resp.content_type.startswith("text/html")


def test_dashboard_page(client):
    """GET /dashboard.html should serve the dashboard HTML."""
    resp = client.get("/dashboard.html")
    assert resp.status_code == 200
