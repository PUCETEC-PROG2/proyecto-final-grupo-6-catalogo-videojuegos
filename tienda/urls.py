from django.urls import path

from . import views
from .views import buscar_productos

app_name = 'tienda'

urlpatterns = [
    path("", views.index, name="index"),
    path("Producto/", views.Productos, name="Producto"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path('buscar/', buscar_productos, name='buscar_productos'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('juegos-usados/', views.juegos_usados, name='juegos_usados'),
    path('consolas-usadas/', views.consolas_usadas, name='consolas_usadas'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path("add_cliente/", views.add_cliente, name="add_cliente"),
    path("edit_cliente/<int:id_cliente>/", views.edit_cliente, name="edit_cliente"),
    path('clientes/eliminar/<int:id_cliente>/', views.delet_cliente, name='delet_cliente'),
    path("add_compra/", views.add_compra, name="add_compra"),
    path('compra/<int:id_compra>/', views.detalle_compra, name='detalle_compra'),
]