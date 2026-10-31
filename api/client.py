"""Thin wrapper around requests: base URL + default timeout in one place."""
import allure
import requests

import config


class ApiClient:
    def __init__(self, base_url=config.API_BASE_URL, timeout=config.DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        with allure.step(f"{method} {path}"):
            response = self.session.request(method, f"{self.base_url}{path}", **kwargs)
            allure.attach(f"{response.status_code} {response.reason}\n\n{response.text}",
                          name="response", attachment_type=allure.attachment_type.TEXT)
            return response

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)
