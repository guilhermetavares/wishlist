from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from pydantic import BaseModel, EmailStr, ValidationError, validator

from client import ProductAPIConsumer
from models import Customer as MongoCustomer

app = FastAPI()


class Customer(BaseModel):
    name: str
    email: str

    @validator('email')
    def name_already_exists(cls, v):
        if MongoCustomer.get_customer(v):
            raise ValueError('Email already taken!')
        return v


class Product(BaseModel):
    uuid: str

    @pydantic.validator('uuid', pre=True, always=True)
    def default_uuid(cls, value):
        response =  ProductAPIConsumer().product(value)
        cls.response = response
        print(response)
        return value


@app.get("/")
def read_root():
    return {"version": "1.0.0"}


@app.post("/customers/{email_or_uuid}/products")
def add_product(email_or_uuid: str, product: Product):
    customer = MongoCustomer.get_customer(email_or_uuid)
    print(product)
    print(product.response)
    return {'O': 'K'}


@app.get("/customers/{email_or_uuid}")
def read_item(email_or_uuid: str, q: str = None):
    customer = MongoCustomer.get_customer(email_or_uuid)

    print('*' * 100)
    print(customer)
    print(customer.to_json())

    if customer:
        return customer.to_json()

    raise HTTPException(status_code=404, detail="Customer not found")


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
