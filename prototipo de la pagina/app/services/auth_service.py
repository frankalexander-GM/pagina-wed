from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def encriptar_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def validar_email_duplicado(email, modelo_usuario):
    # Lógica para buscar si el usuario ya existe
    existe = modelo_usuario.query.filter_by(email=email).first()
    return existe is not None