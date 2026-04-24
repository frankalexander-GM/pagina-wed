"""
Servicio de carrito de compras (session-based)
Maneja operaciones del carrito de compras usando la sesión de Flask
"""
from flask import session


class CarritoService:
    """
    Servicio de carrito de compras basado en sesión
    """
    
    def __init__(self, producto_repo=None):
        self.producto_repo = producto_repo
    
    def get_carrito(self):
        """Obtener carrito actual de la sesión"""
        if 'carrito' not in session:
            session['carrito'] = []
        return session['carrito']
    
    def agregar_producto(self, producto_id, cantidad=1):
        """Agregar producto al carrito"""
        carrito = self.get_carrito()
        
        # Verificar si el producto ya está en el carrito
        for item in carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += cantidad
                session.modified = True
                return True
        
        # Obtener datos del producto
        if self.producto_repo:
            producto = self.producto_repo.get_by_id(producto_id)
            if producto and producto.stock >= cantidad:
                carrito.append({
                    'producto_id': producto_id,
                    'nombre': producto.nombre,
                    'precio': float(producto.precio),
                    'cantidad': cantidad,
                    'imagen': producto.imagen,
                    'artista_nombre': producto.artista.nombre if producto.artista else ''
                })
                session.modified = True
                return True
        return False
    
    def quitar_producto(self, producto_id):
        """Quitar producto del carrito"""
        carrito = self.get_carrito()
        session['carrito'] = [item for item in carrito if item['producto_id'] != producto_id]
        session.modified = True
        return True
    
    def actualizar_cantidad(self, producto_id, cantidad):
        """Actualizar cantidad de un producto en el carrito"""
        if cantidad <= 0:
            return self.quitar_producto(producto_id)
        
        carrito = self.get_carrito()
        for item in carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] = cantidad
                session.modified = True
                return True
        return False
    
    def get_total(self):
        """Obtener total del carrito"""
        carrito = self.get_carrito()
        return sum(item['precio'] * item['cantidad'] for item in carrito)
    
    def get_items_count(self):
        """Obtener cantidad total de items"""
        carrito = self.get_carrito()
        return sum(item['cantidad'] for item in carrito)
    
    def vaciar_carrito(self):
        """Vaciar el carrito"""
        session['carrito'] = []
        session.modified = True
        return True
    
    def get_carrito_detallado(self):
        """Obtener carrito con detalles y totales"""
        carrito = self.get_carrito()
        items = []
        total = 0
        
        for item in carrito:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal
            items.append({
                **item,
                'subtotal': subtotal
            })
        
        return {
            'items': items,
            'total': total,
            'items_count': self.get_items_count()
        }
