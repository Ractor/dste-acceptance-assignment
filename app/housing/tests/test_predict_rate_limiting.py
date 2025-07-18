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

def test_rate_limit_exceeded_in_window(client, clear_rate_limit_storage):
    with patch("security.API_TOKEN", "mock_token"):
        for i in range(10):
            with patch("time.time", return_value=1700000000.00+ i * 3):
                response = client.get(
                    "/housing/predict?" + URL_PARAMS,
                    headers={"Authorization": "Bearer mock_token"}   
                )
                assert response.status_code == 200
        with patch("time.time", return_value=1700000030.00):
            response = client.get(
                "/housing/predict?" + URL_PARAMS,
                headers={"Authorization": "Bearer mock_token"}   
            )
            assert response.status_code == 429
            assert response.json() == {"detail": "Rate limit exceeded"}

def test_rate_limit_ok_in_window(client, clear_rate_limit_storage):
    with patch("security.API_TOKEN", "mock_token"):
        for i in range(10):
            with patch("time.time", return_value=1700000000.00+ i * 3):
                response = client.get(
                    "/housing/predict?" + URL_PARAMS,
                    headers={"Authorization": "Bearer mock_token"}   
                )
                assert response.status_code == 200
        
        with patch("time.time", return_value=1700000061.00):
            response = client.get(
                "/housing/predict?" + URL_PARAMS,
                headers={"Authorization": "Bearer mock_token"}   
            )
            assert response.status_code == 200

def test_rate_limit_exceeded_multiple_ips(client, clear_rate_limit_storage):
    with patch("security.API_TOKEN", "mock_token"):
        for i in range(10):
            with patch("time.time", return_value=1700000000.00+ i * 3):
                response = client.get(
                    "/housing/predict?" + URL_PARAMS,
                    headers={"Authorization": "Bearer mock_token"}   
                )
                assert response.status_code == 200
        for i in range(5):
            with patch("time.time", return_value=1700000000.00+ i * 3):
                response = client.get(
                    "/housing/predict?" + URL_PARAMS,
                    headers={
                        "Authorization": "Bearer mock_token",
                        "X-Forwarded-For": "42.42.42.42",
                    }
                )
                assert response.status_code == 200
        with patch("time.time", return_value=1700000030.00):
            response = client.get(
                "/housing/predict?" + URL_PARAMS,
                headers={"Authorization": "Bearer mock_token"}   
            )
            assert response.status_code == 429
            assert response.json() == {"detail": "Rate limit exceeded"}

            response = client.get(
                "/housing/predict?" + URL_PARAMS,
                headers={
                    "Authorization": "Bearer mock_token",
                    "X-Forwarded-For": "42.42.42.42",
                }  
            )
            assert response.status_code == 200