"""Cross-resource checks that don't belong to one service."""
import pytest


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    "resource, expected_count",
    [("posts", 100), ("comments", 500), ("albums", 100), ("photos", 5000),
     ("todos", 200), ("users", 10)],
)
def test_resource_collection_sizes(api, resource, expected_count):
    response = api.get(f"/{resource}")
    assert response.status_code == 200
    assert len(response.json()) == expected_count
