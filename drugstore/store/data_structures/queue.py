class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        return None if self.is_empty() else self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def list_all(self):
        return self.items
