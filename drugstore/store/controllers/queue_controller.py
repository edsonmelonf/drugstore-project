from store.data_structures.queue import Queue

class QueueController:
    def __init__(self):
        self.queue = Queue()

    def new_order(self, cliente):
        """Adiciona um novo pedido na fila"""
        self.queue.enqueue(cliente)

    def process_order(self):
        """Processa (remove) o próximo pedido da fila"""
        return self.queue.dequeue()

    def list_orders(self):
        """Retorna todos os pedidos na fila sem removê-los"""
        return self.queue.list_all()

    def has_orders(self):
        """Verifica se há pedidos na fila"""
        return not self.queue.is_empty()
