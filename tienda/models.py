from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
class Categoria(models.Model):
    id_catalogo = models.AutoField(primary_key=True)
    CATEGORIA_CHOICES = [
        ('JUEGOS', 'Juegos Usados'),
        ('CONSOLAS', 'Consolas Usadas'),
    ]
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        verbose_name="Categoría"
    )
    class Meta:
        indexes = [
            models.Index(fields=['categoria']),
        ]

    def __str__(self):
        return f"{self.get_categoria_display()}"

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    cedula = models.CharField(
        max_length=20,  
        validators=[
            MinLengthValidator(10, message="La cédula debe tener al menos 10 dígitos."),
            RegexValidator(r'^\d+$', message="La cédula debe contener solo números.")
        ],
        unique=True,  
        verbose_name="Cédula"
    )
    telefono = models.CharField(
        max_length=15,  
        validators=[
            MinLengthValidator(10, message="El número de teléfono debe tener al menos 10 dígitos."),
            RegexValidator(r'^\d+$', message="El número de teléfono debe contener solo números.")
        ],
        verbose_name="Teléfono"
    )
    direccion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['cedula']),
        ]

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    JUEGOS_CHOICES = [
        ('ACCION', 'Accion'),
        ('AVENTURA', 'Aventura'),
        ('DEPORTE', 'deporte'),
        ('RPG', 'rpg'),
        ('ARCADE', 'Arcade'),
        ('PLATAFORMAS', 'Plataformas'),
        ('DISPAROS', 'Disparos'),
    ]
    CONSOLAS_CHOICES = [
        ('PS2', 'Play station 2'),
        ('PS3', 'Play station 3'),
        ('PS4', 'Play station 4'),
        ('PS5', 'Play station 5'),
        ('XBOX', 'Xbox'),
        ('NINTENDO', 'Nintendo Swich'),
    ]
    genero_videojuegos = models.CharField(
        max_length=50,
        choices=JUEGOS_CHOICES,null=True, blank=True,
        verbose_name="Genero videojuegos"
    )
    tipo_consola = models.CharField(
        max_length=50,
        choices=CONSOLAS_CHOICES, null=True, blank=True,
        verbose_name="Consolas de videojuegos"
    )
    imagenes = models.ImageField(upload_to="productos_images")
    class Meta:
        indexes = [
            models.Index(fields=['nombre_producto']),
            models.Index(fields=['precio']),
        ]

    def __str__(self):
        return self.nombre_producto
    
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['producto']),
        ]

    def __str__(self):
        return f"Inventario de {self.producto.nombre}"

class Compras(models.Model):
    id_compra = models.AutoField(primary_key=True)
    productos = models.ManyToManyField(Producto, related_name='Compras')
    comprador = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='Comprador')
    fecha_transaccion = models.DateField()
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_transaccion']),
        ]

    def __str__(self):
        return f"Transacción {self.id_compra} - {self.comprador}"
    
    def calcular_precio_final(self):
        total = sum(producto.precio for producto in self.productos.all())
        self.precio_final = total
        self.save()
        return total

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)