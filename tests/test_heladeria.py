import pytest
from models.heladeria_model import Ingrediente, Producto
from app import app, db

@pytest.fixture
def setup_app():
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_abastecer_ingrediente(setup_app):
    ingrediente = Ingrediente(nombre="Azúcar", cantidad=0)
    db.session.add(ingrediente)
    db.session.commit()

    assert ingrediente.cantidad == 0
    ingrediente.cantidad += 10
    db.session.commit()
    assert ingrediente.cantidad == 10

def test_vender_producto(setup_app):
    ingrediente = Ingrediente(nombre="Leche", cantidad=10)
    producto = Producto(nombre="Malteada", precio=5000, calorias=200, ingrediente_1_id=ingrediente.id)
    db.session.add_all([ingrediente, producto])
    db.session.commit()

    assert ingrediente.cantidad == 10
    producto_id = producto.id
    assert ingrediente.cantidad > 0  # Suficiente para venta
