from flask import render_template, request
from models.heladeria_model import Producto, vender_producto

def home():
    # Consultar productos desde la base de datos
    productos = Producto.query.all()
    menu = [{"nombre": p.nombre, "precio": p.precio} for p in productos]
    return render_template("index.html", menu=menu)


def realizar_venta():
    """
    Maneja la venta de un producto. Devuelve un mensaje según el resultado de la venta.
    """
    producto_id = request.args.get("producto_id") 
    try:
        mensaje = vender_producto(producto_id)
        return f"<h1>{mensaje}</h1>"  
    except ValueError as e:

        return f"<h1>¡Oh no! Nos hemos quedado sin {str(e)}</h1>"