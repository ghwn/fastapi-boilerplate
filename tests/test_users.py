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
            "username": "tester",
        },
    )
    assert response.status_code == 422


def test_create_user_with_username_starting_with_non_alphabet(authorized_client):
    response = authorized_client.post(
        url="/api/v1/users",
        json={
            "username": "_tester",
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user_with_too_short_username(authorized_client):
    response = authorized_client.post(
        url="/api/v1/users",
        json={
            "username": "te",
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user(client):
    response = client.post(
        url="/api/v1/users",
        json={
            "username": "tester",
            "password": "password",
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "tester"
    assert "password" not in response.json()


def test_get_users(authorized_client):
    response = authorized_client.get(url="/api/v1/users")
    assert response.status_code == 200


def test_get_user_404(authorized_client):
    response = authorized_client.get(url="/api/v1/users/nottester")
    assert response.status_code == 404


def test_get_user(authorized_client, user):
    response = authorized_client.get(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 200


def test_update_user_without_password(authorized_client, user):
    response = authorized_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 422


def test_update_user_404(authorized_client):
    response = authorized_client.put(
        url="/api/v1/users/nottester",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 404


def test_update_user(authorized_client, user):
    response = authorized_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 200


def test_patch_user_404(authorized_client):
    response = authorized_client.patch(
        url="/api/v1/users/nottester",
        json={
            "is_active": False,
        },
    )
    assert response.status_code == 404


def test_patch_user(authorized_client, user):
    response = authorized_client.patch(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_active": False,
        },
    )
    assert response.status_code == 200


def test_delete_user_404(authorized_client):
    response = authorized_client.delete(url="/api/v1/users/nottester")
    assert response.status_code == 404


def test_delete_user(authorized_client, user):
    response = authorized_client.delete(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 204
