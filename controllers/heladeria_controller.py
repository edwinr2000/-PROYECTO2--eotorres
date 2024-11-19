from flask import render_template
from models.heladeria_model import Producto

def home():
    # Consultar productos desde la base de datos
    productos = Producto.query.all()
    menu = [{"nombre": p.nombre, "precio": p.precio} for p in productos]
    return render_template("index.html", menu=menu)
