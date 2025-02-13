from django.urls import path

from . import views
from .views import buscar_productos

app_name = 'tienda'

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.Productos, name='productos'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('juegos-usados/', views.juegos_usados, name='juegos_usados'),
    path('consolas-usadas/', views.consolas_usadas, name='consolas_usadas'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path('add-cliente/', views.add_cliente, name='add_cliente'),
    path('edit-cliente/<int:id_cliente>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/eliminar/<int:id_cliente>/', views.delet_cliente, name='delet_cliente'),
    path('add-compra/', views.add_compra, name='add_compra'),
    path('vista-previa-factura/<int:id_compra>/', views.vista_previa_factura, name='vista_previa_factura'),
    path('generar-factura-pdf/<int:id_compra>/', views.generar_factura_pdf, name='generar_factura_pdf'),
]