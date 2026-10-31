from api.services.base_service import BaseService


class UsersService(BaseService):
    path = "/users"

    def posts(self, user_id):
        return self.client.get(f"{self.path}/{user_id}/posts")
