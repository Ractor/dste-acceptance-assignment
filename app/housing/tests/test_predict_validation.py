from urllib.parse import urlencode
from unittest.mock import patch


def _prediction_request(client, urlparams):
    mock_token = "mocked_token"
    with patch("security.API_TOKEN", mock_token):
        return client.get(
            "/housing/predict?" + urlencode(urlparams),
            headers={"Authorization": f"Bearer {mock_token}"},
        )


def test_ok(client, clear_rate_limit_storage):
    urlparams = {
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
    response = _prediction_request(client, urlparams)
    assert response.status_code == 200
    assert response.json() == {"price": 320201.58554043656}


def test_invalid_longitude(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": None,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "float_parsing",
                "loc": ["query", "longitude"],
                "msg": "Input should be a valid number, "
                + "unable to parse string as a number",
                "input": "None",
                "url": "https://errors.pydantic.dev/2.11/v/float_parsing",
            }
        ]
    }


def test_invalid_latitude(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": None,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "float_parsing",
                "loc": ["query", "latitude"],
                "msg": "Input should be a valid number, "
                + "unable to parse string as a number",
                "input": "None",
                "url": "https://errors.pydantic.dev/2.11/v/float_parsing",
            }
        ]
    }


def test_negative_housing_median_age(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": -1.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "housing_median_age"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_negative_total_rooms(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": -1.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "total_rooms"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_negative_total_bedrooms(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": -1.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "total_bedrooms"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_negative_population(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": -1.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "population"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_negative_households(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": -1.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "households"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_negative_median_income(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": -1.0,
        "ocean_proximity": "NEAR OCEAN",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["query", "median_income"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1.0",
                "ctx": {"ge": 0.0},
                "url": "https://errors.pydantic.dev/2.11/v/greater_than_equal",
            }
        ]
    }


def test_invalid_ocean_proximity(client, clear_rate_limit_storage):
    urlparams = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NOT_A_VALID_VALUE",
    }
    response = _prediction_request(client, urlparams)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["query", "ocean_proximity"],
                "msg": "Input should be '<1H OCEAN', 'INLAND', "
                + "'ISLAND', 'NEAR BAY' or 'NEAR OCEAN'",
                "input": "NOT_A_VALID_VALUE",
                "ctx": {
                    "expected": "'<1H OCEAN', 'INLAND', "
                    + "'ISLAND', 'NEAR BAY' or 'NEAR OCEAN'"
                },
                "url": "https://errors.pydantic.dev/2.11/v/enum",
            }
        ]
    }
