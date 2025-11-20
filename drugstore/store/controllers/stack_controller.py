from store.data_structures.stack import Stack

class StackController:
    def __init__(self):
        self.stack = Stack()

    def add_action(self, description):
        self.stack.push(description)

    def undo_action(self):
        return self.stack.pop()

    def get_history(self):
        return self.stack.list_all()
