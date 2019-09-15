from uplink import Consumer, Path, get, json, returns


@json
@returns.json
class ProductAPIConsumer(Consumer):
    URL = 'http://challenge-api.luizalabs.com/api/'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('base_url', self.URL)
        super().__init__(*args, **kwargs)

    @get("product/{uuid}")
    def product(self, uuid: Path):
        pass
