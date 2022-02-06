from app.security import create_access_token


def test_create_user_without_username(user_client):
    response = user_client.post(
        url="/api/v1/users",
        json={
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user_without_password(user_client):
    response = user_client.post(
        url="/api/v1/users",
        json={
            "username": "tester",
        },
    )
    assert response.status_code == 422


def test_create_user_with_username_starting_with_non_alphabet(user_client):
    response = user_client.post(
        url="/api/v1/users",
        json={
            "username": "_tester",
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user_with_too_short_username(user_client):
    response = user_client.post(
        url="/api/v1/users",
        json={
            "username": "te",
            "password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user(guest_client):
    response = guest_client.post(
        url="/api/v1/users",
        json={
            "username": "tester",
            "password": "password",
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "tester"
    assert "password" not in response.json()


def test_get_users_by_user(user_client):
    response = user_client.get(url="/api/v1/users")
    assert response.status_code == 403


def test_get_users_by_superuser(superuser_client):
    response = superuser_client.get(url="/api/v1/users")
    assert response.status_code == 200


def test_get_user_404(superuser_client):
    response = superuser_client.get(url="/api/v1/users/nottester")
    assert response.status_code == 404


def test_get_user_403(user_client, user2):
    response = user_client.get(url=f"/api/v1/users/{user2.username}")
    assert response.status_code == 403


def test_get_user(user_client, user):
    response = user_client.get(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 200


def test_get_other_user(superuser_client, user2):
    response = superuser_client.get(url=f"/api/v1/users/{user2.username}")
    assert response.status_code == 200


def test_update_user_without_password(user_client, user):
    response = user_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 422


def test_update_user_404_by_user(user_client):
    response = user_client.put(
        url="/api/v1/users/nottester",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 403


def test_update_user_404(superuser_client):
    response = superuser_client.put(
        url="/api/v1/users/nottester",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 404


def test_update_user_403(user_client, user):
    response = user_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 403


def test_update_user(superuser_client, user):
    response = superuser_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 200


def test_patch_user_404_by_user(user_client):
    response = user_client.patch(
        url="/api/v1/users/nottester",
        json={
            "is_active": False,
        },
    )
    assert response.status_code == 403


def test_patch_user_itself(user_client, user):
    response = user_client.patch(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_active": False,
        },
    )
    assert response.status_code == 200


def test_patch_user_with_is_superuser_by_user(user_client, user):
    response = user_client.patch(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_superuser": True,
        },
    )
    assert response.status_code == 403


def test_patch_user_with_is_superuser_by_superuser(superuser_client, user):
    response = superuser_client.patch(
        url=f"/api/v1/users/{user.username}",
        json={
            "is_superuser": True,
        },
    )
    assert response.status_code == 200


def test_delete_user_404(user_client):
    response = user_client.delete(url="/api/v1/users/nottester")
    assert response.status_code == 403


def test_delete_user(user_client, user):
    response = user_client.delete(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 204


def test_delete_other(superuser_client, user2):
    response = superuser_client.delete(url=f"/api/v1/users/{user2.username}")
    assert response.status_code == 204


def test_get_users_with_access_token_of_non_existent_user(guest_client, user):
    access_token = create_access_token({"username": "hello"})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.get("/api/v1/users")
    assert response.status_code == 403


def test_get_users_with_access_token_of_inactive_user(guest_client, inactive_user):
    access_token = create_access_token({"username": inactive_user.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.get("/api/v1/users")
    assert response.status_code == 403


def test_get_users_with_access_token_of_inactive_superuser(guest_client, inactive_superuser):
    access_token = create_access_token({"username": inactive_superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.get("/api/v1/users")
    assert response.status_code == 403


def test_get_user_with_access_token_of_inactive_superuser(guest_client, inactive_superuser, user):
    access_token = create_access_token({"username": inactive_superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.get(f"/api/v1/users/{user.username}")
    assert response.status_code == 403


def test_update_user_with_access_token_of_inactive_superuser(
    guest_client, inactive_superuser, user
):
    access_token = create_access_token({"username": inactive_superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.put(
        url=f"/api/v1/users/{user.username}",
        json={
            "password": "password",
            "is_active": False,
            "is_superuser": False,
        },
    )
    assert response.status_code == 403


def test_patch_user_with_access_token_of_inactive_superuser(
    guest_client, inactive_superuser, user
):
    access_token = create_access_token({"username": inactive_superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.patch(
        url=f"/api/v1/users/{user.username}",
        json={"is_active": False},
    )
    assert response.status_code == 403


def test_delete_user_with_access_token_of_inactive_superuser(
    guest_client, inactive_superuser, user
):
    access_token = create_access_token({"username": inactive_superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    response = guest_client.delete(url=f"/api/v1/users/{user.username}")
    assert response.status_code == 403
