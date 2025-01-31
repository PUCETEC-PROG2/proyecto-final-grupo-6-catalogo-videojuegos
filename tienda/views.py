from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import Categoria,Cliente,Producto,Inventario,Compras


# Create your views here.
def index(request):
    productos = Producto.objects.order_by('precio')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'productos': productos}, request))

def Products(request):
    Producto = Producto.objects.all()
    template = loader.get_template('display_products.html')
    return HttpResponse(template.render({'Producto': Producto}, request))

class CustomLoginView(LoginView):
    template_name = "login_form.html"