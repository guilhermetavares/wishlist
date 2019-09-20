import pytest
import uuid

from conftest import get_customer

from app.models import Customer as MongoCustomer


VALID_PRODUCT_UUID = 'ddeb989e-53c4-e68b-aa93-6e43afddb797'
VALID_PRODUCT_UUID_2 = 'de2911eb-ce5c-e783-1ca5-82d0ccd4e3d8'


def test_api_client(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {'version': '1.0.0'}


def test_api_detail_customer(api_client, customer):
    response = api_client.get("/customers/any_invalid_value")
    assert response.status_code == 404

    response = api_client.get(f"/customers/{customer.email}")
    assert response.status_code == 200
    assert response.json()['email'] == customer.email

    response = api_client.get(f"/customers/{customer.uuid}")
    assert response.status_code == 200
    assert response.json()['email'] == customer.email


def test_api_create_customer(api_client):
    data = {
      "name": "name",
      "email": "email@dominio.do.email",
    }
    response = api_client.post(
        "/customers/",
        json=data,
    )
    assert response.status_code == 201
    assert response.json()['email'] == data['email']

    response = api_client.post(
        "/customers/",
        json=data,
    )
    assert response.status_code == 422


def test_api_delete_customer(api_client, customer):
    response = api_client.delete("/customers/any_invalid_value")
    assert response.status_code == 404
    response = api_client.delete(f"/customers/{customer.email}")
    assert response.status_code == 204


def test_api_update_customer(api_client, customer):
    new_customer = get_customer()

    data = {
      "name": "name",
      "email": new_customer.email,
    }

    response = api_client.put(
        "/customers/any_invalid_value",
        json=data,
    )
    assert response.status_code == 404

    response = api_client.put(
        f"/customers/{customer.email}",
        json=data,
    )
    assert response.status_code == 422

    data = {
      "name": "new name",
      "email": "new.email@dominio.do.email",
    }
    response = api_client.put(
        f"/customers/{customer.email}",
        json=data,
    )
    assert response.status_code == 200
    customer.reload()
    assert customer.email == data.get('email')
    assert customer.name == data.get('name')


def test_api_add_products(api_client, customer):

    data = {
        'uuid': 'invalid-uuid'
    }
    response = api_client.post(
        f"/customers/{customer.email}/products",
        json=data,
    )
    assert response.status_code == 422

    data = {
        'uuid': VALID_PRODUCT_UUID,
    }
    response = api_client.post(
        f"/customers/invalid_user_uuid/products",
        json=data,
    )
    assert response.status_code == 404

    response = api_client.post(
        f"/customers/{customer.email}/products",
        json=data,
    )
    assert response.status_code == 201
    assert response.json()['products'][0]['uuid'] == VALID_PRODUCT_UUID

    response = api_client.post(
        f"/customers/{customer.email}/products",
        json=data,
    )
    assert response.status_code == 422


def test_api_delete_products(api_client, customer_with_product):

    response = api_client.delete(
        f"/customers/invalid_uuid/products/invalid_uuid"
    )
    assert response.status_code == 404

    response = api_client.delete(
        f"/customers/{customer_with_product.email}/products/invalid_uuid"
    )
    assert response.status_code == 404

    product_uuid = customer_with_product.products[0].uuid
    response = api_client.delete(
        f"/customers/{customer_with_product.email}/products/{product_uuid}"
    )
    customer_with_product.reload()
    assert response.status_code == 204
    assert len(list(customer_with_product.products)) == 0
