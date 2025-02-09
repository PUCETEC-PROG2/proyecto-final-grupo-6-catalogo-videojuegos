from django.contrib import admin
from .models import Cliente,Producto,Inventario,Compras, DetalleCompra

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin (admin.ModelAdmin):
        pass

@admin.register(DetalleCompra)
class DetalleCompraAdmin (admin.ModelAdmin):
        pass


@admin.register(Producto)
class ProductoAdmin (admin.ModelAdmin):
        pass

@admin.register(Inventario)
class InventarioAdmin (admin.ModelAdmin):
        pass

@admin.register(Compras)
class ComprasAdmin (admin.ModelAdmin):
        pass