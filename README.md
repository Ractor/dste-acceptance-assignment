# DSTE Acceptance Assignment

This repository contains my solution for assignment to be accepted on position of _Python Backend Developer_ at _Deutsche Telekom Services_. Original assignment is specified in `ASSIGNMENT.md`.

## How to run the code

After pushing to GitHub, the code is automatically deployed to Docker Hub as [ractor/dste-acceptance-assignment](https://hub.docker.com/r/ractor/dste-acceptance-assignment). The `latest` tag should correspond with latest commit in the `master` branch.

The most basic way of running the code is following:

```bash
docker container run --rm -it -p 8000:8000 -e RUN_MODE="app" -e API_TOKEN="xyz" ractor/dste-acceptance-assignment
```

Then you can access the code from `localhost:8000`.

You can find documentation at `/redoc`, but sample cURL follows:

```bash
curl 'http://localhost:8000/housing/predict?longitude=-115.73&latitude=33.35&housing_median_age=23.0&total_rooms=1586.0&total_bedrooms=448.0&population=338.0&households=182.0&median_income=1.2132&ocean_proximity=INLAND' \
--header 'Authorization: Bearer xyz'
```

## Configuration options

- `RUN_MODE` – Specifies which part of code should be ran. Use value `app` for FastAPI application or `test` for running the tests (this is also used in pipeline).
- `API_TOKEN` – Use to specify authentization token (to be used as `Authorization: Bearer` header). Main part of application can't be accessed without api token specification.
- `RATE_LIMIT` – Limit of API requests per given period (default: `10`).
- `RATE_PERIOD` – Reset period (seconds) of the rate limit. Works as a sliding window (default: `60`).
