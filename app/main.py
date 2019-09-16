from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from pydantic import BaseModel, EmailStr, ValidationError, validator

from client import ProductAPIConsumer
from models import Customer as MongoCustomer, Product as MongoProduct

app = FastAPI()


class Customer(BaseModel):
    name: str
    email: str
    uuid: str = None

    @validator('email')
    def name_already_exists(cls, v):
        if MongoCustomer.get_customer(v):
            raise ValueError('Email already taken!')
        return v


class Product(BaseModel):
    uuid: str
    email_or_uuid: str = None

    @validator('uuid', pre=True, always=True)
    def default_uuid(cls, value):
        try:
            response =  ProductAPIConsumer().product(value)
        except:
            # jsondecode
            raise ValueError('Product not exists!')

        cls.response = response
        cls.link = f'http://challenge-api.luizalabs.com/api/product/{value}'
        return value


@app.get("/")
def read_root():
    return {"version": "1.0.0"}


@app.post("/customers/{email_or_uuid}/products")
def add_product(*, email_or_uuid: str, product: Product):
    customer = MongoCustomer.get_customer(email_or_uuid)

    if customer.check_product(product.uuid):
        raise HTTPException(status_code=400, detail="Product is already exists for this customer!")

    product = MongoProduct(
        uuid=product.uuid,
        data=product.response,
        link=product.link,
    )
    customer.products.append(product)
    customer.save()
    return customer.to_json()


@app.delete("/customers/{email_or_uuid}/products/{uuid}")
def remove_product(*, email_or_uuid: str, product_uuid: str):
    customer = MongoCustomer.get_customer(email_or_uuid)

    if customer.check_product(product.uuid):
        new_products = [product for product in customer.products if str(product.uuid) != product_uuid]
        customer.products = new_products
        customer.save()
        return JSONResponse(status_code=204, content={"message": "Product deleted!"})

    return JSONResponse(status_code=404, content={"message": "Product not found for this customer!"})


@app.get("/customers/{email_or_uuid}")
def read_item(email_or_uuid: str, q: str = None):
    customer = MongoCustomer.get_customer(email_or_uuid)

    if customer:
        return customer.to_json()

    return JSONResponse(status_code=404, content={"message": "Customer not found"})


@app.delete("/customers/{email_or_uuid}")
def read_item(email_or_uuid: str):
    customer = MongoCustomer.get_customer(email_or_uuid)
    customer.delete()

    if customer:
        return JSONResponse(status_code=204, content={"message": "Item deleted"})

    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get("/customers/")
def read_items(q: str = None):
    print(MongoCustomer.objects())
    return {"q": q}


@app.post("/customers/")
def post_item(*, customer: Customer):
    customer = MongoCustomer(name=customer.name, email=customer.email)
    customer.save()
    return customer.to_json()


@app.put("/customers/{item_id}")
def post_item(item_id: str, customer: Customer):
    return {"item_name": customer.name, "item_id": customer.email}
