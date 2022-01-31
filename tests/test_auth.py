def test_signup(client):
    response = client.post(
        url="/auth/signup",
        json={
            "username": "admin",
            "password": "password",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["access_token"]
    assert response_json["token_type"] == "Bearer"


def test_login(client, user):
    response = client.post(
        url="/auth/login",
        json={
            "username": user.username,
            "password": "password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["access_token"]
    assert response_json["token_type"] == "Bearer"
