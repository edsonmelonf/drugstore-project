from store.data_structures.linked_list import LinkedList
from store.data_structures.hash_table import HashTable

class InventoryController:
    def __init__(self):
        self.inventory = LinkedList()
        self.index = HashTable()

    def add_product(self, name, price, qty):
        product = {
            "name": name,
            "price": price,
            "quantity": qty
        }

        # salva na linkedlist
        self.inventory.add(product)

        # salva na hash table
        self.index.add(name.lower(), product)

    def get_all_products(self):
        return self.inventory.list_all()

    def search(self, name):
        return self.index.get(name.lower())
