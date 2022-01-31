def test_create_subject_without_name(authorized_client):
    response = authorized_client.post(
        url="/api/v1/subjects",
        json={},
    )
    assert response.status_code == 422


def test_create_subject(authorized_client):
    response = authorized_client.post(
        url="/api/v1/subjects",
        json={
            "name": "수학",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "수학"


def test_get_subjects(authorized_client):
    response = authorized_client.get(url="/api/v1/subjects")
    assert response.status_code == 200


def test_get_subject_404(authorized_client):
    response = authorized_client.get(url="/api/v1/subjects/123123")
    assert response.status_code == 404


def test_get_subject(authorized_client, subject):
    response = authorized_client.get(url=f"/api/v1/subjects/{subject.id}")
    assert response.status_code == 200


def test_update_subject_without_name(authorized_client, subject):
    response = authorized_client.put(
        url=f"/api/v1/subjects/{subject.id}",
        json={},
    )
    assert response.status_code == 422


def test_update_subject_404(authorized_client):
    response = authorized_client.put(
        url="/api/v1/subjects/123123",
        json={
            "name": "국어",
        },
    )
    assert response.status_code == 404


def test_update_subject(authorized_client, subject):
    response = authorized_client.put(
        url=f"/api/v1/subjects/{subject.id}",
        json={
            "name": "국어",
        },
    )
    assert response.status_code == 200


def test_patch_subject_404(authorized_client):
    response = authorized_client.patch(
        url="/api/v1/subjects/123123",
        json={
            "name": "영어",
        },
    )
    assert response.status_code == 404


def test_patch_subject(authorized_client, subject):
    response = authorized_client.patch(
        url=f"/api/v1/subjects/{subject.id}",
        json={
            "name": "영어",
        },
    )
    assert response.status_code == 200


def test_delete_subject_404(authorized_client):
    response = authorized_client.delete(url="/api/v1/subjects/123123")
    assert response.status_code == 404


def test_delete_subject(authorized_client, subject):
    response = authorized_client.delete(url=f"/api/v1/subjects/{subject.id}")
    assert response.status_code == 204
