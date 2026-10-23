def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_renders_for_guest(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Evaluate machine learning models" in response.content
