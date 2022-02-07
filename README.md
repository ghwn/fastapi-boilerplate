# FastAPI Boilerplate

![build-badge](https://github.com/ghwn/fastapi-boilerplate/actions/workflows/main.yml/badge.svg)

## Set Up

### Prerequisites

- Python 3.9+
- Poetry 1.1.12+

### Set environments

1. Copy `.env.example` into `.env`.

    ```
    $ cp .env.example .env
    ```

2. Execute the following command to create new secret key.

    ```
    $ openssl rand -hex 32
    d77a166b55473754dcb5ed6cb90fd0a62c0d8107d534308d3fa350905333abb3
    ```

3. Open `.env` and paste the secret key that you just created.

    ```
    SECRET_KEY=d77a166b55473754dcb5ed6cb90fd0a62c0d8107d534308d3fa350905333abb3
    ...
    ```

4. If `DATABASE_URL` is blank, the application by default will use `app.db` of which driver is SQLite.

5. Set `DEBUG=1` if you want to see more logs.

### Create database

```
$ alembic upgrade head
```

## Run Server

```
$ poetry run uvicorn app.main:app --reload
```

## Run Tests
```
$ poetry run pytest
```
