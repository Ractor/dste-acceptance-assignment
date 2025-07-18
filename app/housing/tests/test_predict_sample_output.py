from unittest.mock import patch
from urllib.parse import urlencode


def _sample_output(client, urlparams, price):
    mock_token = "mocked_token"
    with patch("security.API_TOKEN", mock_token):
        response = client.get(
            "/housing/predict?" + urlencode(urlparams),
            headers={"Authorization": f"Bearer {mock_token}"}
        )
        assert response.status_code == 200
        assert response.json() == {"price": price}

def test_predict_sample_output1(client):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN"
    }
    _sample_output(client, urlparams, 320201.58554043656)

def test_predict_sample_output2(client):
    urlparams = {
        "longitude": -115.73,
        "latitude": 33.35,
        "housing_median_age": 23.0,
        "total_rooms": 1586.0,
        "total_bedrooms": 448.0,
        "population": 338.0,
        "households": 182.0,
        "median_income": 1.2132,
        "ocean_proximity": "INLAND"
    }
    _sample_output(client, urlparams, 58815.45033764739)

def test_predict_sample_output3(client):
    urlparams = {
        "longitude": -117.96,
        "latitude": 33.89,
        "housing_median_age": 24.0,
        "total_rooms": 1332.0,
        "total_bedrooms": 252.0,
        "population": 625.0,
        "households": 230.0,
        "median_income": 4.4375,
        "ocean_proximity": "<1H OCEAN"
    }
    _sample_output(client, urlparams, 192575.77355634805)



