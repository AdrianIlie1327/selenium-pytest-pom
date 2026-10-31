from api.services.base_service import BaseService


class PostsService(BaseService):
    path = "/posts"

    def comments(self, post_id):
        return self.client.get(f"{self.path}/{post_id}/comments")
