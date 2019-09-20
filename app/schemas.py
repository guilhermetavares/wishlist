from pydantic import BaseModel, EmailStr, ValidationError, validator
from models import Customer as MongoCustomer
from client import ProductAPIConsumer


class BaseCustomer(BaseModel):
    name: str
    email: str


class Customer(BaseCustomer):

    @validator('email')
    def name_already_exists(cls, v):
        if MongoCustomer.get_customer(v):
            raise ValueError('Email already taken!')
        return v


class Product(BaseModel):
    uuid: str

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
