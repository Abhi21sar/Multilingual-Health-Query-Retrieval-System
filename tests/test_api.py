from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

# Mock the entire DataManager and VectorEngine for testing without loading model
# This ensures tests are fast and don't require the 500MB+ model file
@patch('app.services.vector_engine.VectorEngine.get_instance')
def test_health_check(mock_engine):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@patch('app.services.vector_engine.VectorEngine.get_instance')
def test_search_api(mock_engine_factory):
    # Setup Mock
    mock_engine = MagicMock()
    mock_engine.search.return_value = [
        {"Query": "Test Query", "Answer": "Test Answer", "confidence": 95.5}
    ]
    mock_engine_factory.return_value = mock_engine

    response = client.get("/api/v1/search?query=flu")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "flu"
    assert len(data["results"]) == 1
    assert data["results"][0]["confidence"] == 95.5

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "MediQuery Pro" in response.text
