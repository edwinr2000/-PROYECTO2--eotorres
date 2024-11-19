from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, default=0)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Float, nullable=False)
    # Relación con ingredientes
    ingrediente_1_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    ingrediente_2_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    ingrediente_3_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))

# Métodos para la lógica del negocio
def abastecer_ingrediente(ingrediente_id, cantidad):
    ingrediente = Ingrediente.query.get(ingrediente_id)
    if ingrediente:
        ingrediente.cantidad += cantidad
        db.session.commit()
        return f"Ingrediente {ingrediente.nombre} abastecido con éxito."
    else:
        return "Ingrediente no encontrado."

def vender_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        raise ValueError("Producto no encontrado.")
    
    ingredientes = [
        producto.ingrediente_1_id,
        producto.ingrediente_2_id,
        producto.ingrediente_3_id,
    ]
    for ingrediente_id in ingredientes:
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente.cantidad <= 0:
            raise ValueError(f"Falta {ingrediente.nombre} para preparar el producto.")
        ingrediente.cantidad -= 1
    
    db.session.commit()
    return "¡Vendido!"
