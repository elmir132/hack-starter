from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
PAYLOAD = {
    "project_name": "Campus Cart",
    "audience": "students living on campus",
    "problem": "finding a ride home after late labs",
    "approach": "match students with open seats heading the same way",
}


def test_health_is_explicit_about_the_no_model_mode():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "mode": "deterministic-template", "model_configured": False}


def test_create_brief_returns_structured_result():
    response = client.post("/api/brief", json=PAYLOAD)

    assert response.status_code == 200
    result = response.json()
    assert result["project_name"] == PAYLOAD["project_name"]
    assert len(result["mvp"]) == 3
    assert result["model_used"] is False


def test_request_is_trimmed_and_blank_input_is_rejected():
    trimmed = dict(PAYLOAD, project_name="  Campus Cart  ")
    assert client.post("/api/brief", json=trimmed).json()["project_name"] == "Campus Cart"

    blank = dict(PAYLOAD, audience="   ")
    assert client.post("/api/brief", json=blank).status_code == 422


def test_static_fallback_is_served_with_security_headers():
    response = client.get("/")

    assert response.status_code == 200
    assert "small enough to test" in response.text
    assert "content-security-policy" in response.headers
