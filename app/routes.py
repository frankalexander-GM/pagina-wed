from flask import Blueprint, render_template

# ETIQUETA: CONFIGURACIÓN PARA QUE FLASK RECONOZCA LAS RUTAS
routes = Blueprint('routes', __name__)

# --- HISTORIA DE USUARIO: PÁGINA DE INICIO (HOME) ---
@routes.route('/')
def home():
    # Esta ruta busca el archivo home.html en la carpeta templates
    return render_template('home.html')

# --- HISTORIA DE USUARIO: INICIO DE SESIÓN (LOGIN) ---
@routes.route('/login')
def login():
    return render_template('login.html')

# --- RUTA PARA EL INTERIOR (DASHBOARD) ---
@routes.route('/dashboard')
def dashboard():
    return render_template('index.html')