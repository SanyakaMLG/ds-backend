import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError


class ImageProviderClient:
    def __init__(self, host):
        self.host = host

    def get_image(self, id: int):
        try:
            res = requests.get(
                f'{self.host}/images/{id}',
                timeout=2
            )
        except (ConnectionError, ConnectTimeout, ReadTimeout):
            return None, 500

        return res, res.status_code

