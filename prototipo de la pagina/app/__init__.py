from flask import Flask
from .routes import routes  # Importamos el Blueprint que está arriba

def create_app():
    app = Flask(__name__)

    # Registramos las rutas
    app.register_blueprint(routes)

    return app