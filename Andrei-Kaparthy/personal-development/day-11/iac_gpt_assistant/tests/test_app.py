import json
from unittest.mock import patch

import pytest
from app import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the home page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"IaC GPT Assistant" in response.data


@patch("app.process_iac_request")
def test_api_generate_success(mock_process_iac_request, client):
    """Test the /api/generate endpoint with a successful request."""
    # Mock the return value of the core logic function
    mock_process_iac_request.return_value = {
        "user_request": "test request",
        "terraform_code": "some code",
        "report": "# Report\nThis is a test report.",
    }

    response = client.post(
        "/api/generate",
        data=json.dumps({"request": "test request"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["user_request"] == "test request"
    assert data["terraform_code"] == "some code"
    assert "<h1>Report</h1>" in data["report_html"]  # Check for HTML conversion
    mock_process_iac_request.assert_called_once_with("test request")


def test_api_generate_no_request(client):
    """Test the /api/generate endpoint with missing 'request' key."""
    response = client.post(
        "/api/generate",
        data=json.dumps({"wrong_key": "test"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No request provided"


def test_api_generate_not_json(client):
    """Test the /api/generate endpoint with a non-JSON request."""
    response = client.post(
        "/api/generate", data="this is not json", content_type="text/plain"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Request must be JSON"


@patch("app.process_iac_request")
def test_api_generate_processing_error(mock_process_iac_request, client):
    """Test the /api/generate endpoint when the backend logic returns an error."""
    mock_process_iac_request.return_value = {"error": "Something went wrong"}

    response = client.post(
        "/api/generate",
        data=json.dumps({"request": "test request"}),
        content_type="application/json",
    )

    assert response.status_code == 200  # The API call itself is successful
    data = response.get_json()
    assert data["error"] == "Something went wrong"

