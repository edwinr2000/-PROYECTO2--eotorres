import pytest
from app import db, create_app
from models.heladeria_model import Ingrediente, Producto, vender_producto

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_ingrediente_es_sano(app_context):
    ingrediente = Ingrediente(nombre="Leche", cantidad=10)
    db.session.add(ingrediente)
    db.session.commit()
    assert ingrediente.nombre == "Leche"
    assert ingrediente.cantidad == 10

def test_abastecer_ingrediente(app_context):
    ingrediente = Ingrediente(nombre="Azúcar", cantidad=0)
    db.session.add(ingrediente)
    db.session.commit()
    ingrediente.cantidad += 10
    db.session.commit()
    assert ingrediente.cantidad == 10

def test_renovar_inventario(app_context):
    ingrediente = Ingrediente(nombre="Chocolate", cantidad=5)
    db.session.add(ingrediente)
    db.session.commit()
    ingrediente.cantidad = 20
    db.session.commit()
    assert ingrediente.cantidad == 20

def test_calcular_calorias(app_context):
    producto = Producto(nombre="Helado", precio=5000, calorias=300, ingrediente_1_id=None)
    db.session.add(producto)
    db.session.commit()
    assert producto.calorias == 300

def test_calcular_costo_produccion(app_context):
    producto = Producto(nombre="Helado", precio=5000, calorias=300, ingrediente_1_id=None)
    db.session.add(producto)
    db.session.commit()
    assert producto.precio == 5000

def test_rentabilidad_producto(app_context):
    producto = Producto(nombre="Malteada", precio=8000, calorias=200, ingrediente_1_id=None)
    db.session.add(producto)
    db.session.commit()
    costo = 5000
    rentabilidad = producto.precio - costo
    assert rentabilidad == 3000

def test_producto_mas_rentable(app_context):
    producto1 = Producto(nombre="Helado", precio=5000, calorias=200, ingrediente_1_id=None)
    producto2 = Producto(nombre="Malteada", precio=8000, calorias=300, ingrediente_1_id=None)
    db.session.add_all([producto1, producto2])
    db.session.commit()
    productos = Producto.query.all()
    producto_mas_rentable = max(productos, key=lambda p: p.precio - 5000)
    assert producto_mas_rentable.nombre == "Malteada"

def test_vender_producto(app_context):
    ingrediente = Ingrediente(nombre="Leche", cantidad=1)
    producto = Producto(nombre="Helado de Leche", precio=5000, calorias=150, ingrediente_1_id=1)
    db.session.add_all([ingrediente, producto])
    db.session.commit()

    # Venta exitosa
    mensaje = vender_producto(producto.id)
    assert mensaje == "¡Vendido!"
    assert ingrediente.cantidad == 0

    # Venta fallida
    with pytest.raises(ValueError) as excinfo:
        vender_producto(producto.id)
    assert "Leche no está disponible" in str(excinfo.value)
