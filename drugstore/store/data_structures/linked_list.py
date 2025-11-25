class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new = Node(data)
        if not self.head:
            self.head = new
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new

    def list_all(self):
        current = self.head
        items = []
        while current:
            items.append(current.data)
            current = current.next
        return items