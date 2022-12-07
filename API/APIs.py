import requests
import json


class APIs:
    def __init__(self, base_url="https://petstore3.swagger.io/api/v3"):
        self.base_url = base_url
        self.headrs = {'accept': 'application/json'}
        self.session = requests.session()
        self.session.headers.update(self.headrs)

    def get(self, path, expected_status=200):
        res = self.session.get(url=f"{self.base_url}/{path}")
        if res.status_code == expected_status:
            return res.json()
        return res.status_code

    def post(self, path, body, expected_status=200):
        res = self.session.post(url=f"{self.base_url}/{path}", data=body)
        if res.status_code == expected_status:
            return res.json()
        return res.status_code
