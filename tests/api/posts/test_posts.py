import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_list_posts_returns_100_posts(posts):
    response = posts.list()
    assert response.status_code == 200
    assert len(response.json()) == 100


@pytest.mark.api
@pytest.mark.smoke
def test_get_single_post(posts):
    response = posts.get(1)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert {"userId", "title", "body"} <= body.keys()


@pytest.mark.api
@pytest.mark.regression
def test_response_is_json(posts):
    response = posts.get(1)
    assert "application/json" in response.headers["Content-Type"]


@pytest.mark.api
@pytest.mark.regression
def test_filter_posts_by_user(posts):
    response = posts.list(userId=3)
    assert response.status_code == 200
    items = response.json()
    assert items, "expected at least one post for user 3"
    assert all(post["userId"] == 3 for post in items)


@pytest.mark.api
@pytest.mark.regression
def test_get_comments_for_post(posts):
    response = posts.comments(1)
    assert response.status_code == 200
    comments = response.json()
    assert comments
    assert all(comment["postId"] == 1 for comment in comments)


@pytest.mark.api
@pytest.mark.regression
def test_create_post_echoes_payload(posts):
    payload = {"title": "hello", "body": "demo body", "userId": 1}
    response = posts.create(payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 101  # JSONPlaceholder always assigns the next id
    assert {k: body[k] for k in payload} == payload


@pytest.mark.api
@pytest.mark.regression
def test_update_post(posts):
    payload = {"id": 1, "title": "updated", "body": "new body", "userId": 1}
    response = posts.update(1, payload)
    assert response.status_code == 200
    assert response.json() == payload


@pytest.mark.api
@pytest.mark.regression
def test_delete_post(posts):
    response = posts.delete(1)
    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.api
@pytest.mark.negative
def test_unknown_post_returns_404(posts):
    response = posts.get(99999)
    assert response.status_code == 404
