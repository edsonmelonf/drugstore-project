from store.data_structures.stack import Stack

class OrderController:
    def __init__(self):
        self.orders = Stack()

    def new_order(self, cart_items):
        self.orders.push(cart_items)

    def undo_last_order(self):
        return self.orders.pop()

    def list_orders(self):
        return self.orders.list_all()
