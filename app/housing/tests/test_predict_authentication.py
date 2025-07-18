from urllib.parse import urlencode

URL_PARAMS = urlencode(
    {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
)


def test_ok(client, clear_rate_limit_storage):
    response = client.get(
        "/housing/predict?" + URL_PARAMS,
        headers={"Authorization": "Bearer mock_token"},
    )
    assert response.status_code == 200


def test_invalid_token(client, clear_rate_limit_storage):
    response = client.get(
        "/housing/predict?" + URL_PARAMS,
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_missing_header(client, clear_rate_limit_storage):
    response = client.get(
        "/housing/predict?" + URL_PARAMS,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_invalid_header_format(client, clear_rate_limit_storage):
    response = client.get(
        "/housing/predict?" + URL_PARAMS,
        headers={"Authorization": "Token mock_token"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid authentication credentials"}


def test_missing_bearer_keyword(client, clear_rate_limit_storage):
    response = client.get(
        "/housing/predict?" + URL_PARAMS,
        headers={"Authorization": "mock_token"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
