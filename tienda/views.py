from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


from .models import Categoria,Cliente,Producto, Compras,DetalleCompra
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
def add_compra(request):
    if request.method == "POST":
        form = ComprasForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.save()

            # Guardar los productos seleccionados en DetallesCompras
            productos_ids = request.POST.getlist('productos[]')
            cantidades = request.POST.getlist('cantidades[]')

            for prod_id, cantidad in zip(productos_ids, cantidades):
                if not prod_id:  # Si el id del producto está vacío, se salta
                    continue
                producto = Producto.objects.get(id_producto=prod_id)  
                compra.productos.add(producto, through_defaults={'cantidad': cantidad})

            return redirect('tienda:compras')  # Redirigir a la lista de compras

    else:
        form = ComprasForm()
    
    clientes = Cliente.objects.all()  # Asegurar que hay clientes disponibles
    productos = Producto.objects.all()  # Obtener productos disponibles

    return render(request, "compras_form.html", {
        "form": form,
        "clientes": clientes,
        "productos": productos,
    })

def vista_previa_factura(request, id_compra):
    compra = get_object_or_404(Compras, id_compra=id_compra)
    detalles = DetalleCompra.objects.filter(compra=compra)

    total = sum(detalle.producto.precio * detalle.cantidad for detalle in detalles)

    return render(request, 'detalle_compra.html', {
        'compra': compra,
        'detalles': detalles,
        'total': total
    })

def generar_factura_pdf(request, id_compra):
    compra = get_object_or_404(Compras, id_compra=id_compra)
    detalles = DetalleCompra.objects.filter(compra=compra)

    # Configurar la respuesta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{id_compra}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    
    # Datos de la factura
    p.drawString(100, 770, "MUCHAS GRACIAS POR REALIZAR SU COMPRA")
    p.drawString(100, 760, "======================================")
    p.drawString(100, 750, f"Factura de Compra #{id_compra}")
    p.drawString(100, 730, f"Cliente: {compra.comprador}")
    p.drawString(100, 710, f"Fecha: {compra.fecha_transaccion.strftime('%Y-%m-%d')}")
    
    # Encabezados de tabla
    y = 680
    p.drawString(100, y, "Producto")
    p.drawString(300, y, "Cantidad")
    p.drawString(400, y, "Precio")
    y -= 20
    
    # Listado de productos
    total = 0
    for detalle in detalles:
        p.drawString(100, y, detalle.producto.nombre_producto)
        p.drawString(300, y, str(detalle.cantidad))
        p.drawString(400, y, f"${detalle.producto.precio:.2f}")
        total += detalle.producto.precio * detalle.cantidad
        y -= 20
    
    # Total
    p.drawString(100, y - 20, f"Total: ${total:.2f}")
    p.drawString(100, y - 40, "Vuelva Pronto y disfrute de horas de diversión")

    # Dibujar una carita feliz dentro de un círculo
    x_face, y_face, radius = 250, y - 80, 30  # Posición y tamaño del círculo
    p.circle(x_face, y_face, radius)  # Cara

    # Ojos (pequeños círculos)
    p.circle(x_face - 10, y_face + 10, 3)  # Ojo izquierdo
    p.circle(x_face + 10, y_face + 10, 3)  # Ojo derecho

    # Sonrisa (arco)
    p.arc(x_face - 10, y_face - 5, x_face + 10, y_face + 5, 200, 140)  

    # Finalizar y enviar
    p.showPage()
    p.save()
    return response

class CustomLoginView(LoginView):
    template_name = "login_form.html"