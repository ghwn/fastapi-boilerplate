import pytest


def test_create_user(authorized_client):
    response = authorized_client.post(
        url="/api/v1/users",
        json={
            "username": "admin",
            "password": "password",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["username"] == "admin"
    with pytest.raises(KeyError):
        response_json["password"]
    assert response_json["is_active"] is True
    assert response_json["is_superuser"] is False


def test_create_user_without_username(authorized_client):
    response = authorized_client.post(
        url="/api/v1/users",
        json={
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user_without_password(authorized_client):
    response = authorized_client.post(
        url="/api/v1/users",
        json={
            "username": "admin",
        },
    )
    assert response.status_code == 422


def test_get_users(authorized_client, user):
    response = authorized_client.get(url="/api/v1/users")
    assert response.status_code == 200


def test_get_users_with_limit_0(authorized_client, user):
    response = authorized_client.get(url="/api/v1/users?limit=0")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_users_with_limit_1(authorized_client, user):
    response = authorized_client.get(url="/api/v1/users?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user(authorized_client, user):
    response = authorized_client.get(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 200
    assert response.json()["username"] == user.username


def test_get_user_404(authorized_client):
    response = authorized_client.get(url="/api/v1/users/notuser")
    assert response.status_code == 404
