from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Categoria,Cliente,Producto,Inventario,Compras
from tienda.forms import ClienteForm, ComprasForm

# Create your views here.
def index(request):
    productos = Producto.objects.order_by('precio')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'productos': productos}, request))

def Productos(request):
    Producto = Producto.objects.all()
    template = loader.get_template('display_products.html')
    return HttpResponse(template.render({'Producto': Producto}, request))

def buscar_productos(request):
    q = request.GET.get('q', '') 
    productos = Producto.objects.filter(nombre_producto__icontains=q) if q else Producto.objects.all()
    return render(request, 'resultados_busqueda.html', {'productos': productos, 'query': q})

def acerca_de(request):
    return render(request, 'about.html')

def juegos_usados(request):
    categoria = Categoria.objects.get(categoria='JUEGOS')
    productos = Producto.objects.filter(categoria=categoria)    
    return render(request, 'juegos_usados.html', {'productos': productos})


def consolas_usadas(request):
    categoria_consolas = Categoria.objects.get(categoria="CONSOLAS")
    productos_consolas = Producto.objects.filter(categoria=categoria_consolas)
    return render(request, 'consolas_usadas.html', {'productos': productos_consolas})

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def compras(request):
    compras = Compras.objects.all().order_by('-fecha_transaccion')  
    return render(request, 'compras.html', {'compras': compras})

@login_required
def add_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tienda:clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes_form.html', {'form':form})

@login_required
def edit_cliente(request, id_cliente):
    cliente = Cliente.objects.get(pk = id_cliente)
    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('tienda:clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes_form.html', {'form':form})

@login_required
def delet_cliente(request, id_cliente):
    cliente = Cliente.objects.get(pk = id_cliente)
    cliente.delete()
    messages.success(request, f'El cliente "{cliente.nombre}" ha sido eliminado exitosamente.')
    return redirect('tienda:clientes')

@login_required
def detalle_compra(request, id_compra):
    compra = Compras.objects.get(id_compra=id_compra)
    return render(request, 'detalle_compra.html', {'compra': compra})

@login_required
def add_compra(request):
    if request.method == "POST":
        form = ComprasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tienda:compras')
    else:
        form = ComprasForm()

    return render(request, 'compras_form.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = "login_form.html"