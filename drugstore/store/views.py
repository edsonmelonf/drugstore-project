from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

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
    search_result = None

    if query:
        result_dict = inventory_controller.search(query)
        if result_dict:
            class ProductObj:
                def __init__(self, data):
                    self.name = data["name"]
                    self.price = data["price"]
                    self.quantity = data["quantity"]
            search_result = ProductObj(result_dict)

    produtos = Produto.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, "store/home.html", {
        "products": produtos,
        "cart_count": cart_count,
        "search_query": query,
        "search_result": search_result
    })

# ========================= BUSCA =========================

def search_products(request):
    query = request.GET.get("q", "")
    results = Produto.objects.filter(name_product__icontains=query)
    return render(request, "store/search_results.html", {
        "query": query,
        "results": results
    })

# ================= LINKEDLIST + HASH TABLE =================

@user_passes_test(is_admin)
def adicionar_estoque(request):
    """Adiciona quantidade ao estoque usando o formulário AdicionarEstoqueForm"""
    if request.method == "POST":
        form = AdicionarEstoqueForm(request.POST)
        if form.is_valid():
            produto = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']
            produto.quantity += quantidade
            produto.save()
            return redirect('store:listar_estoque')
    else:
        form = AdicionarEstoqueForm()
    return render(request, 'store/add_estoque.html', {'form': form})

@user_passes_test(is_admin)
def listar_estoque(request):
    produtos = inventory_controller.get_all_products()
    return render(request, "store/listar_estoque.html", {"produtos": produtos})

@user_passes_test(is_admin)
def buscar_produto(request):
    resultados = []
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip().lower()
        todos_produtos = inventory_controller.get_all_products()
        for p in todos_produtos:
            if nome in p['name'].lower():
                resultados.append(p)
    return render(request, "store/buscar_produto.html", {"resultados": resultados})

# ========================= QUEUE (FILA) =========================

@user_passes_test(is_admin)
def fila_pedidos(request):
    pedidos = queue_controller.list_orders()
    return render(request, "store/fila.html", {"pedidos": pedidos})

@user_passes_test(is_admin)
def novo_pedido(request):
    if request.method == "POST":
        cliente = request.POST.get("cliente")
        queue_controller.new_order(cliente)
        stack_controller.add_action(f"Novo pedido criado para {cliente}")
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