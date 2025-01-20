# Generated by Django 4.2 on 2025-01-20 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_auto_20250119_2225'),
    ]

    operations = [
         migrations.RunSQL(
            """
            CREATE OR REPLACE PROCEDURE ingreso_cliente(nombre_param TEXT, correo_param TEXT, cedula_param TEXT, telefono_param TEXT, direccion_param TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO tienda_cliente (nombre, correo, cedula, telefono, direccion)
                VALUES (nombre_param, correo_param, cedula_param, telefono_param, direccion_param);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE actualizacion_cliente(id_cliente_param INT, nuevo_nombre TEXT, nuevo_correo TEXT, nueva_cedula TEXT, nuevo_telefono TEXT, nueva_direccion TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tienda_cliente
                SET nombre = nuevo_nombre, correo = nuevo_correo, cedula = nueva_cedula, telefono = nuevo_telefono, direccion = nueva_direccion
                WHERE id_cliente = id_cliente_param;
            END;
            $$;

            CREATE OR REPLACE PROCEDURE ingreso_producto(nombre_producto_param TEXT, descripcion_param TEXT, precio_param NUMERIC, categoria_param INT, genero_videojuegos_param TEXT, tipo_consola_param TEXT, imagenes_param TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO tienda_producto (nombre_producto, descripcion, precio, categoria_id, genero_videojuegos, tipo_consola, imagenes)
                VALUES (nombre_producto_param, descripcion_param, precio_param, categoria_param, genero_videojuegos_param, tipo_consola_param, imagenes_param);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE actualizacion_producto(id_producto_param INT, nuevo_nombre_producto TEXT, nueva_descripcion TEXT, nuevo_precio NUMERIC, nueva_categoria INT, nuevo_genero_videojuegos TEXT, nuevo_tipo_consola TEXT, nuevas_imagenes TEXT)
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tienda_producto
                SET nombre_producto = nuevo_nombre_producto, descripcion = nueva_descripcion, precio = nuevo_precio, categoria_id = nueva_categoria, genero_videojuegos = nuevo_genero_videojuegos, tipo_consola = nuevo_tipo_consola, imagenes = nuevas_imagenes
                WHERE id_producto = id_producto_param;
            END;
            $$;

            CREATE OR REPLACE PROCEDURE ingreso_inventario(producto_param INT, cantidad_param INT)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO tienda_inventario (producto_id, cantidad_disponible)
                VALUES (producto_param, cantidad_param);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE actualiza_inventario(id_inventario_param INT, nueva_cantidad INT)
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tienda_inventario
                SET cantidad_disponible = nueva_cantidad
                WHERE id_inventario = id_inventario_param;
            END;
            $$;

            CREATE OR REPLACE PROCEDURE realizar_compra(comprador_param INT, precio_final_param NUMERIC)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO tienda_compras (comprador_id, precio_final, fecha_transaccion)
                VALUES (comprador_param, precio_final_param, CURRENT_DATE);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE realizar_compra(comprador_param INT, precio_final_param NUMERIC, fecha_param DATE DEFAULT CURRENT_DATE)
            LANGUAGE plpgsql AS $$
            BEGIN
                INSERT INTO tienda_compras (comprador_id, precio_final, fecha_transaccion)
                VALUES (comprador_param, precio_final_param, fecha_param);
            END;
            $$;

            CREATE OR REPLACE PROCEDURE listar_productos()
            LANGUAGE plpgsql AS $$
            BEGIN
                PERFORM id_producto, nombre_producto, descripcion, precio, categoria_id, genero_videojuegos, tipo_consola FROM tienda_producto;
            END;
            $$;
            """
        ),
    ]
