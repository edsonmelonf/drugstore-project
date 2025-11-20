from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # estoque
    path('add/', views.add_estoque, name="add_estoque"),
    path('estoque/', views.listar_estoque, name="listar_estoque"),
    path('buscar/', views.buscar_produto, name="buscar_produto"),

    # fila
    path('fila/', views.fila_pedidos, name="fila_pedidos"),
    path('novo_pedido/', views.novo_pedido, name="novo_pedido"),
    path('processar/', views.processar_pedido, name="processar_pedido"),

    # histórico
    path('historico/', views.historico, name="historico"),
    path('desfazer/', views.desfazer, name="desfazer"),
]
