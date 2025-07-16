FROM python:3.10

WORKDIR /usr/src/app
EXPOSE 8080

RUN apt-get update
RUN apt-get install -y build-essential python3-dev python3.11-dev cython3

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY ./app .

ENV RUN_MODE=none

RUN useradd --no-create-home --shell /usr/sbin/nologin --password "*" appuser
USER appuser

ENTRYPOINT [ "/bin/sh", "./entrypoint.sh" ]