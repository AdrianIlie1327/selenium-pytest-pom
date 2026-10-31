import pytest

from api.client import ApiClient
from api.services.posts import PostsService
from api.services.users import UsersService


@pytest.fixture
def api():
    """HTTP client for API tests (no browser is started)."""
    return ApiClient()


@pytest.fixture
def posts(api):
    return PostsService(api)


@pytest.fixture
def users(api):
    return UsersService(api)
