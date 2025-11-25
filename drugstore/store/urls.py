from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # HOME
    path('', views.home, name="home"),

    # BUSCA (necessário porque a home chama store:search_products)
    path('search/', views.search_products, name="search_products"),

    # ESTOQUE (LinkedList + Hash Table)
    path('estoque/', views.listar_estoque, name="listar_estoque"),
    path('buscar/', views.buscar_produto, name="buscar_produto"),
    path('add_estoque/', views.adicionar_estoque, name='add_estoque'),

    # FILA (Queue)
    path('fila/', views.fila_pedidos, name="fila_pedidos"),
    path('novo_pedido/', views.novo_pedido, name="novo_pedido"),
    path('processar/', views.processar_pedido, name="processar_pedido"),

    # HISTÓRICO (Stack)
    path('historico/', views.historico, name="historico"),
    path('desfazer/', views.desfazer, name="desfazer"),

    path('criar_produto/', views.criar_produto, name='criar_produto'),

]
