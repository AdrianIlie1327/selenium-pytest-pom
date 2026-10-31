"""Shared CRUD calls. Services return the raw Response; tests do the asserting."""


class BaseService:
    path = ""  # set in subclasses, e.g. "/posts"

    def __init__(self, client):
        self.client = client

    def list(self, **params):
        return self.client.get(self.path, params=params)

    def get(self, item_id):
        return self.client.get(f"{self.path}/{item_id}")

    def create(self, payload):
        return self.client.post(self.path, json=payload)

    def update(self, item_id, payload):
        return self.client.put(f"{self.path}/{item_id}", json=payload)

    def delete(self, item_id):
        return self.client.delete(f"{self.path}/{item_id}")
