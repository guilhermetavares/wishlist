import pytest

from client import ProductAPIConsumer


@pytest.mark.vcr()
def test_product_client():
    value = 'ddeb989e-53c4-e68b-aa93-6e43afddb797'
    response = ProductAPIConsumer().product(value)
    assert response['id'] == value
