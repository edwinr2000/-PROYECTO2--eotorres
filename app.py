from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from controllers.heladeria_controller import home
from models.heladeria_model import db

# Configuración de la base de datos
DB_USER = "root"
DB_PASSWORD = "142000"
DB_HOST = "localhost"
DB_NAME = "heladeria"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos
db.init_app(app)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# Rutas
@app.route("/")
def index():
    return home()

if __name__ == "__main__":
    app.run(debug=True)
