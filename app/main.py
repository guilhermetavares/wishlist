import uuid
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse

from models import Customer as MongoCustomer, Product as MongoProduct
from schemas import BaseCustomer, Customer, Product


API_USER = os.environ.get('API_USER', None)
API_PASSWORD = os.environ.get('API_PASSWORD', None)


app = FastAPI()
security = HTTPBasic(realm="simple")


# TODO: see future decorator options
def assert_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not all([credentials.username==API_USER, credentials.password==API_PASSWORD]):
        raise HTTPException(status_code=401, detail="Invalid credentials!")


@app.get("/")
def api_version(credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    return {
        "version": "1.0.0",
    }


@app.get("/customers/{uuid_or_email}")
def get_customer(uuid_or_email: str, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Get the customer detail by customer uuid or email.
    If the customer exists, the api will return code 200 and show all customer data.
    If not, the api will return code 404.
    '''
    customer = MongoCustomer.get_customer(uuid_or_email)

    if customer:
        return customer.api_json()

    return JSONResponse(status_code=404, content={"message": "Customer not found"})


@app.delete("/customers/{uuid_or_email}")
def delete_customer(uuid_or_email: str, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Delete the customer if the customer exists and return code 204
    If not, the api will return code 404.
    '''

    customer = MongoCustomer.get_customer(uuid_or_email)

    if customer:
        customer.delete()
        return JSONResponse(status_code=204, content={"message": "Customer deleted"})

    return JSONResponse(status_code=404, content={"message": "Customer not found"})


@app.post("/customers/")
def create_customer(*, customer: Customer, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Create a new customer, if the post data succeed the schema validation.
    If succeed, return the new customer data with code 201.
    If not, return a validation error on api.
    '''
    customer = MongoCustomer(
        uuid=uuid.uuid1(),
        name=customer.name,
        email=customer.email)
    customer.save()
    return JSONResponse(status_code=201, content=customer.api_json())


@app.put("/customers/{uuid_or_email}")
def update_customer(uuid_or_email: str, data: BaseCustomer, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Update the customer data by customer uuid or email.
    If the customer exists, the api will update customer data and return all customer data and code 200.
    If not, the api will return code 404.
    If the email is already taken, the api return code 422.
    '''

    customer = MongoCustomer.get_customer(uuid_or_email)

    if customer is None:
        return JSONResponse(status_code=404, content={"message": "Customer not found"})

    if customer.email != data.email and MongoCustomer.get_customer(data.email):
        return JSONResponse(status_code=422, content={"message": "Email already taken!"})

    customer.email = data.email
    customer.name = data.name
    customer.save()
    return JSONResponse(status_code=200, content=customer.api_json())


@app.post("/customers/{uuid_or_email}/products")
def add_product(*, uuid_or_email: str, product: Product, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Add a new product for customer wishlist.
    If all validation succeed, return all customer data with code 201.
    If not, return a validation error on api or code 404.
    '''
    customer = MongoCustomer.get_customer(uuid_or_email)

    if customer is None:
        return JSONResponse(status_code=404, content={"message": "Customer not found"})

    if customer.check_product(product.uuid):
        return JSONResponse(status_code=422, content={"message": "Product already exists for this customer!"})

    product = MongoProduct(
        uuid=product.uuid,
        data=product.response,
        link=product.link,
    )
    customer.products.append(product)
    customer.save()
    return JSONResponse(status_code=201, content=customer.api_json())


@app.delete("/customers/{email_or_uuid}/products/{product_uuid}")
def remove_product(email_or_uuid: str, product_uuid: str, credentials: HTTPBasicCredentials = Depends(assert_credentials)):
    '''
    Remove a product for customer wishlist.
    If all validation succeed, return code 204.
    If not, return a validation error on api or code 404.
    '''

    customer = MongoCustomer.get_customer(email_or_uuid)

    if customer is None:
        return JSONResponse(status_code=404, content={"message": "Customer not found"})

    if customer.check_product(product_uuid):
        new_products = [product for product in customer.products if str(product.uuid) != product_uuid]
        customer.products = new_products
        customer.save()
        return JSONResponse(status_code=204, content={"message": "Product deleted!"})

    return JSONResponse(status_code=404, content={"message": "Product not found for this customer!"})
