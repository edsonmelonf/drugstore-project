from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from order.models import Order


from .controllers.inventory_controller import InventoryController
from .controllers.queue_controller import QueueController
from .controllers.stack_controller import StackController
from .models import Produto
from .forms import AdicionarEstoqueForm

# ---- Restrição para staff/admin ----

def is_admin(user):
    return user.is_authenticated and user.is_staff

# ---- Instâncias das estruturas ----

inventory_controller = InventoryController()
queue_controller = QueueController()
stack_controller = StackController()

# ========================= HOME =========================


def home(request):
    query = request.GET.get("q", "").strip()

    if query:
        produtos = Produto.objects.filter(
            Q(name_product__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    else:
        produtos = Produto.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, "store/home.html", {
        "products": produtos,
        "cart_count": cart_count,
        "search_query": query,
    })


# ========================= BUSCA =========================

def search_products(request):
    query = request.GET.get('q', '').strip()
    products = Produto.objects.none()

    if query:
        products = Produto.objects.filter(
            Q(name_product__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    return render(request, 'store/home.html', {
        'query': query,
        'products': products,
    })
# ================= LINKEDLIST + HASH TABLE =================

@user_passes_test(is_admin)
def adicionar_estoque(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        price = float(request.POST.get("price"))
        qty = int(request.POST.get("qty"))
        inventory_controller.add_product(name, price, qty)
        return redirect("store:listar_estoque")
    return render(request, "store/add_estoque.html")

@user_passes_test(is_admin)
@user_passes_test(is_admin)
def listar_estoque(request):
    query = ""
    resultados = []

    if request.method == "POST":
        query = request.POST.get("nome", "").strip().lower()
        if query:
            produto = inventory_controller.search(query)
            if produto:
                resultados.append(produto)

    produtos = inventory_controller.get_all_products()
    return render(request, "store/listar_estoque.html", {
        "produtos": produtos,
        "resultados": resultados,
        "query": query
    })


@user_passes_test(is_admin)
def buscar_produto(request):
    query = request.POST.get("nome", "").strip().lower()
    resultados = []
    if query:
        produto = inventory_controller.search(query)
        if produto:
            resultados.append(produto)
    return render(request, "store/buscar_produto.html", {"resultados": resultados, "query": query})

# ========================= QUEUE (FILA) =========================

@user_passes_test(is_admin)
def fila_pedidos(request):
    pedidos = Order.objects.all().order_by("created_at")
    return render(request, "store/fila.html", {"pedidos": pedidos})

@user_passes_test(is_admin)

@user_passes_test(is_admin)
def novo_pedido(request):

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        total = request.POST.get("total")

        pedido = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total=total
        )

        queue_controller.new_order(pedido)
        stack_controller.add_action(f"Novo pedido criado para {full_name}")
        return redirect("store:fila_pedidos")

    return render(request, "store/novo_pedido.html")

@user_passes_test(is_admin)
def processar_pedido(request):
    if queue_controller.has_orders():
        pedido = queue_controller.process_order()
        msg = f"Processou pedido de {pedido}"
    else:
        pedido = None
        msg = "Nenhum pedido para processar"
    stack_controller.add_action(msg)
    return redirect("store:fila_pedidos")

# ========================= STACK (HISTÓRICO) =========================

@user_passes_test(is_admin)
def historico(request):
    hist = stack_controller.get_history()
    return render(request, "store/historico.html", {"historico": hist})

@user_passes_test(is_admin)
def desfazer(request):
    stack_controller.undo_action()
    return redirect("store:historico")

# ========================= PRODUTO =========================

@user_passes_test(is_admin)
def criar_produto(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = float(request.POST.get("price", 0))
        description = request.POST.get("description", "")
        image = request.FILES.get("image", None)

        # Salva no banco de dados
        Produto.objects.create(
            name_product=name,
            price=price,
            description=description,
            image_product=image
        )

        # Salva na estrutura de dados
        inventory_controller.add_product(name, price, 0)

        # Histórico
        stack_controller.add_action(f"Produto criado: {name}")

        return redirect("store:listar_estoque")

    return render(request, "store/criar_produto.html")

# ========================= CLASSES AUXILIARES =========================

class ProductObj:
    def __init__(self, data):
        self.name = data["name"]
        self.price = data["price"]
        self.quantity = data["quantity"]