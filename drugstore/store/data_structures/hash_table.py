class HashTable:
    def __init__(self):
        self.table = {}

    def add(self, key, value):
        self.table[key] = value

    def get(self, key):
        return self.table.get(key)

    def list_all(self):
        return self.table.items()