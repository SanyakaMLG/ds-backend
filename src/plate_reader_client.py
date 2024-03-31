import json

import requests
from image_provider_client import ImageProviderClient


class PlateReaderClient:
    def __init__(self, host: str, image_provider_client: ImageProviderClient):
        self.host = host
        self.image_provider_client = image_provider_client

    def _read_plate_number(self, id: int):
        im, status = self.image_provider_client.get_image(id)

        if status == 404:
            return {'image_id': id, 'error': 'invalid image id'}
        if str(status).startswith('5'):
            return {'image_id': id, 'error': 'image providing service is unavailable'}

        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return {'image_id': id} | res.json()

    def read_plate_number(self, id: int):
        return json.dumps(self._read_plate_number(id), ensure_ascii=False)

    def read_multiple_plate_numbers(self, ids: list[int]):
        res = []
        for id in ids:
            res.append(self._read_plate_number(id))

        return json.dumps(res, ensure_ascii=False)


if __name__ == '__main__':
    img_client = ImageProviderClient(host='http://178.154.220.122:7777')
    client = PlateReaderClient(host='http://127.0.0.1:8080',
                               image_provider_client=img_client)
    res = client.read_plate_number(10022)
    print(res)

    res = client.read_multiple_plate_numbers([10022, 10022, 9965, 1000, 9965])
    print(res)
