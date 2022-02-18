# def test_login(guest_client, user):
#     response = guest_client.post(
#         url="/auth/token",
#         json={
#             "username": user.username,
#             "password": "password",
#         },
#     )
#     assert response.status_code == 200
#
#     response_json = response.json()
#     assert response_json["access_token"]
#     assert response_json["token_type"] == "Bearer"
