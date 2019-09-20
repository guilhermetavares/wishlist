import pytest
import uuid

from starlette.testclient import TestClient
from app.main import app

from app.schemas import Product
from app.models import Customer as MongoCustomer, Product as MongoProduct


@pytest.fixture
def api_client():
    client = TestClient(app)
    return client


def get_customer():
    uuid_dt = uuid.uuid1()
    name = f'{uuid_dt}'
    email = f'{name}@email.com'

    customer = MongoCustomer(
        uuid=uuid_dt,
        name=name,
        email=email)
    customer.save()
    return customer


@pytest.fixture
def customer():
    return get_customer()


@pytest.fixture
def customer_with_product():
    product = Product(**{'uuid': 'd6d56f1d-61f4-325a-e356-c92968b72a09'})
    customer = get_customer()

    product = MongoProduct(
        uuid=product.uuid,
        data=product.response,
        link=product.link,
    )
    customer.products.append(product)
    customer.save()
    return customer
