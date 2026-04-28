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
    
    try:
        # Obtener datos del dashboard
        stats = {
            'siguiendo_count': usuario_service.get_siguiendo_count(current_user.id_usuario),
            'favoritos_count': obra_service.get_favoritos_count(current_user.id_usuario),
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
    except Exception as e:
        print(f"Error en dashboard de cliente: {e}")
        flash('Error al cargar el dashboard', 'error')
        return redirect(url_for('public.home'))

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
    try:
        service_factory = get_service_factory()
        # TODO: Obtener lienzos del usuario cuando el servicio esté listo
        # Por ahora mostramos lista vacía
        lienzos = []
        return render_template('cliente/lienzos.html', lienzos=lienzos)
    except Exception as e:
        print(f"Error al cargar lienzos: {e}")
        flash('Error al cargar tus lienzos', 'error')
        return redirect(url_for('cliente.dashboard'))

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
    try:
        # TODO: Obtener direcciones reales cuando el servicio esté completamente listo
        direcciones = []
        return render_template('cliente/direcciones.html', direcciones=direcciones)
    except Exception as e:
        print(f"Error al cargar direcciones: {e}")
        flash('Error al cargar tus direcciones', 'error')
        return redirect(url_for('cliente.dashboard'))

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
    try:
        service_factory = get_service_factory()
        # TODO: Obtener órdenes reales cuando el servicio esté listo
        ordenes = []
        return render_template('cliente/ordenes.html', ordenes=ordenes)
    except Exception as e:
        print(f"Error al cargar órdenes: {e}")
        flash('Error al cargar tus órdenes', 'error')
        return redirect(url_for('cliente.dashboard'))

@cliente_bp.route('/carrito')
@login_required
@requiere_cliente
def carrito():
    """
    Carrito de compras
    """
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    
    items, total = carrito_service.get_items()
    count = carrito_service.get_count()
    
    return render_template('cliente/carrito.html', items=items, total=total, count=count)

@cliente_bp.route('/carrito/actualizar/<int:producto_id>', methods=['POST'])
@login_required
@requiere_cliente
def actualizar_carrito(producto_id):
    """
    Actualizar cantidad de un producto en el carrito
    """
    cantidad = request.form.get('cantidad', type=int)
    
    if cantidad is not None:
        service_factory = get_service_factory()
        carrito_service = service_factory.get_carrito_service()
        carrito_service.actualizar_cantidad(producto_id, cantidad)
        flash('Carrito actualizado', 'success')
        
    return redirect(url_for('cliente.carrito'))

@cliente_bp.route('/carrito/remover/<int:producto_id>', methods=['POST'])
@login_required
@requiere_cliente
def remover_carrito(producto_id):
    """
    Remover producto del carrito
    """
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    carrito_service.remover_producto(producto_id)
    flash('Producto eliminado del carrito', 'success')
    
    return redirect(url_for('cliente.carrito'))

@cliente_bp.route('/checkout')
@login_required
@requiere_cliente
def checkout():
    """
    Proceso de pago
    """
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    
    items, total = carrito_service.get_items()
    count = carrito_service.get_count()
    
    if count == 0:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('cliente.carrito'))
        
    # Obtener direcciones del usuario (simulado para el MVP)
    direcciones = []
    
    return render_template('cliente/checkout.html', items=items, total=total, count=count, direcciones=direcciones)

@cliente_bp.route('/checkout/procesar', methods=['POST'])
@login_required
@requiere_cliente
def procesar_checkout():
    """
    Procesar pago de la orden
    """
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    
    # Validar carrito
    items, total = carrito_service.get_items()
    if not items:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('cliente.carrito'))
        
    # Simular procesamiento de pago exitoso para el MVP
    # En un sistema real aquí se llamaría al servicio de Stripe/PayPal y luego a orden_service
    
    # Vaciar carrito
    carrito_service.vaciar_carrito()
    
    flash('¡Compra realizada con éxito! Tu orden está siendo procesada.', 'success')
    return redirect(url_for('cliente.ordenes'))

@cliente_bp.route('/newsletters')
@login_required
@requiere_cliente
def newsletters():
    """
    Newsletters recibidos (bandeja de entrada)
    """
    try:
        service_factory = get_service_factory()
        newsletter_service = service_factory.get_newsletter_service()
        
        # Obtener newsletters del usuario
        newsletters = newsletter_service.get_by_usuario(current_user.id_usuario)
        
        return render_template('cliente/newsletters.html', newsletters=newsletters)
    except Exception as e:
        print(f"Error al cargar newsletters: {e}")
        flash('Error al cargar tus newsletters', 'error')
        return redirect(url_for('cliente.dashboard'))

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
    
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    exitoso = carrito_service.agregar_producto(producto_id, cantidad)
    
    return jsonify({
        'exitoso': exitoso,
        'mensaje': 'Producto agregado al carrito' if exitoso else 'Error al agregar'
    })

@cliente_bp.route('/api/carrito/quitar', methods=['POST'])
@login_required
@requiere_cliente
def quitar_carrito():
    """
    API para quitar producto del carrito
    """
    producto_id = request.json.get('producto_id')
    
    service_factory = get_service_factory()
    carrito_service = service_factory.get_carrito_service()
    exitoso = carrito_service.remover_producto(producto_id)
    
    return jsonify({
        'exitoso': exitoso,
        'mensaje': 'Producto quitado del carrito' if exitoso else 'Error al quitar'
    })
