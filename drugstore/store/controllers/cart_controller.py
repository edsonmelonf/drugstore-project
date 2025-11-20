from store.data_structures.queue import Queue

class CartController:
    def __init__(self):
        self.cart = Queue()

    def add_to_cart(self, product):
        self.cart.enqueue(product)

    def remove_from_cart(self):
        return self.cart.dequeue()

    def get_items(self):
        return self.cart.list_all()
