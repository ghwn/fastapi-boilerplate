FROM python:3.9-slim-buster

RUN mkdir /code

COPY pyproject.toml /code

WORKDIR /code

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /code
