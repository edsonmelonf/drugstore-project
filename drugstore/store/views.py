from django.shortcuts import render, redirect

from .controllers.inventory_controller import InventoryController
from .controllers.queue_controller import QueueController
from .controllers.stack_controller import StackController

inventory_controller = InventoryController()
queue_controller = QueueController()
stack_controller = StackController()

# HOME
def home(request):
    products = inventory_controller.get_all_products()
    return render(request, "store/home.html", {"products": products})


# ---------------- LINKEDLIST + HASH TABLE ----------------

def add_estoque(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = float(request.POST["price"])
        qty = int(request.POST["qty"])

        inventory_controller.add_product(name, price, qty)

        # adiciona no histórico (stack)
        stack_controller.add_action(f"Adicionou {qty} unidades de {name}")

        return redirect("listar_estoque")

    return render(request, "store/add_estoque.html")

def listar_estoque(request):
    produtos = inventory_controller.get_all_products()
    return render(request, "store/listar_estoque.html", {"produtos": produtos})

def buscar_produto(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        produto = inventory_controller.search(nome)
        return render(request, "store/buscar_produto.html", {"produto": produto})
    
    return render(request, "store/buscar_produto.html")

# ---------------- QUEUE (FILA) ----------------

def fila_pedidos(request):
    pedidos = queue_controller.list_orders()
    return render(request, "store/fila.html", {"pedidos": pedidos})

def novo_pedido(request):
    if request.method == "POST":
        cliente = request.POST["cliente"]

        queue_controller.new_order(cliente)
        stack_controller.add_action(f"Novo pedido criado para {cliente}")

        return redirect("fila_pedidos")
    
    return render(request, "store/novo_pedido.html")

def processar_pedido(request):
    pedido = queue_controller.process_order()

    stack_controller.add_action(f"Processou pedido de {pedido}" if pedido else "Nenhum pedido para processar")

    return redirect("fila_pedidos")

# ---------------- STACK (HISTÓRICO) ----------------

def historico(request):
    hist = stack_controller.get_history()
    return render(request, "store/historico.html", {"historico": hist})

def desfazer(request):
    resultado = stack_controller.undo_action()
    return redirect("historico")
