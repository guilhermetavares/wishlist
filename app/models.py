import mongoengine
import os

from mongoengine import connect
from mongoengine.queryset.visitor import Q


MONGO_HOST = os.environ.get('MONGO_HOST', None)
MONGO_USER = os.environ.get('MONGO_USER', None)
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', None)
MONGO_DATABASE = os.environ.get('MONGO_DATABASE', None)

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

    def check_product(self, uuid):
        return uuid in [i.uuid for i in self.products]

    @classmethod
    def get_customer(self, key):
        return Customer.objects(email=key).first() # Q(uuid=key) | Q(email=key))
