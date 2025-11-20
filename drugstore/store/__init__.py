from store.data_structures.linked_list import LinkedList

class InventoryController:
    def __init__(self):
        self.inventory = LinkedList()

        # Remédios pré-carregados
        initial_products = [
            {"name": "Dipirona", "price": 5.99, "quantity": 50},
            {"name": "Paracetamol", "price": 7.49, "quantity": 40},
            {"name": "Ibuprofeno", "price": 12.90, "quantity": 35},
            {"name": "Amoxicilina", "price": 24.90, "quantity": 20},
            {"name": "Loratadina", "price": 9.50, "quantity": 30},
            {"name": "Omeprazol", "price": 14.99, "quantity": 25},
            {"name": "Neosaldina", "price": 8.99, "quantity": 60},
            {"name": "Benegrip", "price": 6.49, "quantity": 45},
            {"name": "Rivotril", "price": 32.90, "quantity": 12},
            {"name": "Buscopan", "price": 11.49, "quantity": 33}
        ]

        for product in initial_products:
            self.inventory.add(product)

    def add_product(self, name, price, qty):
        self.inventory.add({
            "name": name,
            "price": price,
            "quantity": qty
        })

    def get_all_products(self):
        return self.inventory.list_all()
