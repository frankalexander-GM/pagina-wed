from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.factories.service_factory import get_service_factory
from functools import wraps

# Crear blueprint
cliente_bp = Blueprint('cliente', __name__)

def requiere_cliente(f):
    """Decorador para requerir rol de cliente"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_cliente():
            flash('Esta página es solo para clientes', 'error')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated_function

@cliente_bp.route('/dashboard')
@login_required
@requiere_cliente
def dashboard():
    """
    Dashboard del cliente
    """
    service_factory = get_service_factory()
    usuario_service = service_factory.get_usuario_service()
    obra_service = service_factory.get_obra_service()
    
    # Obtener datos del dashboard
    stats = {
        'artistas_siguiendo': usuario_service.get_siguiendo_count(current_user.id_usuario),
        'obras_favoritas': obra_service.get_favoritos_count(current_user.id_usuario),
        'lienzos_count': 0,  # TODO: Implementar cuando tengamos moodboards
        'ordenes_count': 0   # TODO: Implementar cuando tengamos e-commerce
    }
    
    # Obtener artistas que sigue
    artistas_siguiendo = usuario_service.get_siguiendo(current_user.id_usuario, limit=6)
    
    # Obtener obras favoritas
    obras_favoritas = obra_service.get_favoritos_usuario(current_user.id_usuario, limit=6)
    
    return render_template('cliente/dashboard.html',
                         stats=stats,
                         artistas_siguiendo=artistas_siguiendo,
                         obras_favoritas=obras_favoritas)

@cliente_bp.route('/perfil')
@login_required
@requiere_cliente
def perfil():
    """
    Perfil del cliente
    """
    return render_template('cliente/perfil.html')

@cliente_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
@requiere_cliente
def editar_perfil():
    """
    Editar perfil del cliente
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        data = {
            'nombre': request.form.get('nombre'),
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'biografia': request.form.get('biografia', '')
        }
        
        # Validar y actualizar
        service_factory = get_service_factory()
        usuario_service = service_factory.get_usuario_service()
        
        exitoso, usuario_actualizado = usuario_service.actualizar_usuario(current_user.id_usuario, data)
        
        if exitoso:
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('cliente.perfil'))
        else:
            flash('Error al actualizar el perfil', 'error')
    
    return render_template('cliente/editar_perfil.html')

@cliente_bp.route('/artistas-siguiendo')
@login_required
@requiere_cliente
def artistas_siguiendo():
    """
    Listado de artistas que sigue el cliente
    """
    service_factory = get_service_factory()
    usuario_service = service_factory.get_usuario_service()
    
    # Obtener artistas que sigue
    artistas = usuario_service.get_siguiendo(current_user.id_usuario)
    
    return render_template('cliente/artistas_siguiendo.html', artistas=artistas)

@cliente_bp.route('/obras-favoritas')
@login_required
@requiere_cliente
def obras_favoritas():
    """
    Listado de obras favoritas del cliente
    """
    service_factory = get_service_factory()
    obra_service = service_factory.get_obra_service()
    
    # Obtener obras favoritas
    obras = obra_service.get_favoritos_usuario(current_user.id_usuario)
    
    return render_template('cliente/obras_favoritas.html', obras=obras)

@cliente_bp.route('/lienzos')
@login_required
@requiere_cliente
def lienzos():
    """
    Moodboards del cliente
    """
    return render_template('cliente/lienzos.html')

@cliente_bp.route('/lienzos/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_cliente
def nuevo_lienzo():
    """
    Crear nuevo moodboard
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        
        if not nombre.strip():
            flash('El nombre del lienzo es obligatorio', 'error')
            return render_template('cliente/nuevo_lienzo.html')
        
        # TODO: Implementar creación de lienzo cuando tengamos el servicio
        flash('Lienzo creado correctamente', 'success')
        return redirect(url_for('cliente.lienzos'))
    
    return render_template('cliente/nuevo_lienzo.html')

@cliente_bp.route('/direcciones')
@login_required
@requiere_cliente
def direcciones():
    """
    Direcciones de envío del cliente
    """
    return render_template('cliente/direcciones.html')

@cliente_bp.route('/direcciones/nueva', methods=['GET', 'POST'])
@login_required
@requiere_cliente
def nueva_direccion():
    """
    Agregar nueva dirección
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        data = {
            'id_usuario': current_user.id_usuario,
            'nombre_receptor': request.form.get('nombre_receptor'),
            'direccion': request.form.get('direccion'),
            'ciudad': request.form.get('ciudad'),
            'pais': request.form.get('pais'),
            'codigo_postal': request.form.get('codigo_postal'),
            'telefono': request.form.get('telefono')
        }
        
        # Validar datos
        errores = []
        campos_obligatorios = ['nombre_receptor', 'direccion', 'ciudad', 'pais']
        
        for campo in campos_obligatorios:
            if not data.get(campo, '').strip():
                errores.append(f'El campo {campo} es obligatorio')
        
        if not errores:
            # TODO: Implementar servicio de direcciones
            flash('Dirección agregada correctamente', 'success')
            return redirect(url_for('cliente.direcciones'))
        else:
            for error in errores:
                flash(error, 'error')
    
    return render_template('cliente/nueva_direccion.html')

@cliente_bp.route('/ordenes')
@login_required
@requiere_cliente
def ordenes():
    """
    Historial de órdenes del cliente
    """
    return render_template('cliente/ordenes.html')

@cliente_bp.route('/carrito')
@login_required
@requiere_cliente
def carrito():
    """
    Carrito de compras
    """
    return render_template('cliente/carrito.html')

@cliente_bp.route('/checkout')
@login_required
@requiere_cliente
def checkout():
    """
    Proceso de pago
    """
    return render_template('cliente/checkout.html')

@cliente_bp.route('/newsletters')
@login_required
@requiere_cliente
def newsletters():
    """
    Newsletters recibidos
    """
    return render_template('cliente/newsletters.html')

# API endpoints
@cliente_bp.route('/api/seguir-artista', methods=['POST'])
@login_required
@requiere_cliente
def seguir_artista():
    """
    API para seguir/dejar de seguir a un artista
    """
    artista_id = request.json.get('artista_id')
    accion = request.json.get('accion')  # 'seguir' o 'dejar_seguir'
    
    service_factory = get_service_factory()
    usuario_service = service_factory.get_usuario_service()
    
    if accion == 'seguir':
        exitoso = usuario_service.seguir_artista(current_user.id_usuario, artista_id)
        mensaje = 'Ahora sigues a este artista' if exitoso else 'Error al seguir artista'
    else:
        exitoso = usuario_service.dejar_de_seguir_artista(current_user.id_usuario, artista_id)
        mensaje = 'Has dejado de seguir a este artista' if exitoso else 'Error al dejar de seguir artista'
    
    return jsonify({
        'exitoso': exitoso,
        'mensaje': mensaje
    })

@cliente_bp.route('/api/favorito-obra', methods=['POST'])
@login_required
@requiere_cliente
def favorito_obra():
    """
    API para agregar/quitar obra de favoritos
    """
    obra_id = request.json.get('obra_id')
    accion = request.json.get('accion')  # 'agregar' o 'quitar'
    
    service_factory = get_service_factory()
    obra_service = service_factory.get_obra_service()
    
    if accion == 'agregar':
        exitoso = obra_service.agregar_favorito(current_user.id_usuario, obra_id)
        mensaje = 'Obra agregada a favoritos' if exitoso else 'Error al agregar a favoritos'
    else:
        exitoso = obra_service.quitar_favorito(current_user.id_usuario, obra_id)
        mensaje = 'Obra quitada de favoritos' if exitoso else 'Error al quitar de favoritos'
    
    return jsonify({
        'exitoso': exitoso,
        'mensaje': mensaje
    })

@cliente_bp.route('/api/carrito/agregar', methods=['POST'])
@login_required
@requiere_cliente
def agregar_carrito():
    """
    API para agregar producto al carrito
    """
    producto_id = request.json.get('producto_id')
    cantidad = request.json.get('cantidad', 1)
    
    # TODO: Implementar servicio de carrito
    return jsonify({
        'exitoso': True,
        'mensaje': 'Producto agregado al carrito'
    })

@cliente_bp.route('/api/carrito/quitar', methods=['POST'])
@login_required
@requiere_cliente
def quitar_carrito():
    """
    API para quitar producto del carrito
    """
    producto_id = request.json.get('producto_id')
    
    # TODO: Implementar servicio de carrito
    return jsonify({
        'exitoso': True,
        'mensaje': 'Producto quitado del carrito'
    })
