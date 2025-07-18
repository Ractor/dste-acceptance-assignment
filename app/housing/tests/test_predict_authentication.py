from urllib.parse import urlencode
from unittest.mock import patch

URL_PARAMS = urlencode({
    "longitude": -122.64,
    "latitude": 38.01,
    "housing_median_age": 36.0,
    "total_rooms": 1336.0,
    "total_bedrooms": 258.0,
    "population": 678.0,
    "households": 249.0,
    "median_income": 5.5789,
    "ocean_proximity": "NEAR OCEAN"
})

def test_ok(client):
    with patch("security.API_TOKEN", "mock_token"):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
            headers={"Authorization": "Bearer mock_token"}   
        )
    assert response.status_code == 200

def test_invalid_token(client):
    with patch("security.API_TOKEN", "mock_token"):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
            headers={"Authorization": "Bearer invalid_token"}   
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

def test_missing_header(client):
    with patch("security.API_TOKEN", "mock_token"):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}

def test_invalid_header_format(client):
    with patch("security.API_TOKEN", "mock_token"):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
            headers={"Authorization": "Token mock_token"}   
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Invalid authentication credentials"}

def test_missing_bearer_keyword(client):
    with patch("security.API_TOKEN", "mock_token"):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
            headers={"Authorization": "mock_token"}   
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}

def test_api_token_not_set(client):
    with patch("security.API_TOKEN", None):
        response = client.get(
            "/housing/predict?" + URL_PARAMS,
            headers={"Authorization": "mock_token"}   
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}

