import mongoengine
import os

from mongoengine import connect
from mongoengine.queryset.visitor import Q


MONGO_HOST = os.environ['MONGO_HOST']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_DATABASE = os.environ['MONGO_DATABASE']

connect(
    db=MONGO_DATABASE,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    host='{}?authSource=admin'.format(MONGO_HOST),
)


class Product(mongoengine.EmbeddedDocument):
    uuid = mongoengine.UUIDField()
    data = mongoengine.DictField()
    link = mongoengine.StringField()


class Customer(mongoengine.Document):
    uuid = mongoengine.UUIDField()
    name = mongoengine.StringField()
    email = mongoengine.EmailField(primary_key=True)
    products = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Product))

    @classmethod
    def get_customer(self, key):
        return Customer.objects(email=key).first() # Q(uuid=key) | Q(email=key))
