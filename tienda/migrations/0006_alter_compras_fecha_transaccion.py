# Generated by Django 4.2 on 2025-02-06 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_alter_producto_genero_videojuegos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compras',
            name='fecha_transaccion',
            field=models.DateField(),
        ),
    ]
