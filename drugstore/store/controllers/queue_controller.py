from store.data_structures.queue import Queue

class QueueController:
    def __init__(self):
        self.queue = Queue()

    def new_order(self, customer_name):
        self.queue.enqueue(customer_name)

    def process_order(self):
        return self.queue.dequeue()

    def list_orders(self):
        return self.queue.list_all()
