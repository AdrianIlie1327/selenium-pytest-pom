import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_list_users_returns_10_users(users):
    response = users.list()
    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.api
@pytest.mark.regression
def test_get_single_user(users):
    response = users.get(1)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert {"name", "username", "email", "address", "company"} <= body.keys()


@pytest.mark.api
@pytest.mark.regression
def test_user_posts_belong_to_user(users):
    response = users.posts(1)
    assert response.status_code == 200
    items = response.json()
    assert items
    assert all(post["userId"] == 1 for post in items)


@pytest.mark.api
@pytest.mark.negative
def test_unknown_user_returns_404(users):
    assert users.get(99999).status_code == 404
