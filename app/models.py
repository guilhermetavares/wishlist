import mongoengine
import os
import json
import uuid

MONGO_HOST = os.environ.get('MONGO_HOST', None)
MONGO_USER = os.environ.get('MONGO_USER', None)
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', None)
MONGO_DATABASE = os.environ.get('MONGO_DATABASE', None)


mongoengine.connect(
    db=MONGO_DATABASE,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    host='{}?authSource=admin'.format(MONGO_HOST),
)


class Product(mongoengine.EmbeddedDocument):
    uuid = mongoengine.UUIDField(binary=False)
    data = mongoengine.DictField()
    link = mongoengine.StringField()


class Customer(mongoengine.Document):
    uuid = mongoengine.UUIDField(binary=False)
    name = mongoengine.StringField()
    email = mongoengine.EmailField(unique=True)
    products = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Product))

    def api_json(self):
        return json.loads(self.to_json())

    def check_product(self, uuid):
        return uuid in [str(i.uuid) for i in self.products]

    @classmethod
    def get_customer(self, key):

        try:
            uuid.UUID(key)
            params = {'uuid': key}
        except ValueError:
            params = {'email': key}

        return Customer.objects(**params).first()
