from common.request_util import request_util

class BaseApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return request_util.send_request(method, url, **kwargs)
