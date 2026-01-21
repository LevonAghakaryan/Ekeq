from app.repositories import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, order_data):
        return self.repo.create(order_data)

    def get_all_orders(self):
        return self.repo.get_all()

    def get_order_by_id(self, order_id: int):
        return self.repo.get_by_id(order_id)

    def update_order_status(self, order_id: int, new_status: str):
        return self.repo.update_status(order_id, new_status)