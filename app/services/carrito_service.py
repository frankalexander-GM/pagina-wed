"""
Servicio de carrito de compras
Maneja operaciones del carrito guardado en la sesión
"""
from flask import session

class CarritoService:
    """Servicio de carrito de compras basado en sesión"""
    
    def __init__(self, producto_repo=None):
        self.producto_repo = producto_repo
        
    def _get_cart(self):
        """Obtener carrito de la sesión"""
        if 'carrito' not in session:
            session['carrito'] = {}
        return session['carrito']
        
    def _save_cart(self):
        """Guardar carrito en la sesión (marcar como modificada)"""
        session.modified = True
        
    def agregar_producto(self, producto_id, cantidad=1):
        """Agregar producto al carrito"""
        carrito = self._get_cart()
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str] += cantidad
        else:
            carrito[producto_id_str] = cantidad
            
        self._save_cart()
        return True
        
    def remover_producto(self, producto_id):
        """Remover producto del carrito"""
        carrito = self._get_cart()
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            del carrito[producto_id_str]
            self._save_cart()
            return True
        return False
        
    def actualizar_cantidad(self, producto_id, cantidad):
        """Actualizar cantidad de un producto"""
        carrito = self._get_cart()
        producto_id_str = str(producto_id)
        
        if cantidad <= 0:
            return self.remover_producto(producto_id)
            
        if producto_id_str in carrito:
            carrito[producto_id_str] = cantidad
            self._save_cart()
            return True
        return False
        
    def vaciar_carrito(self):
        """Vaciar todo el carrito"""
        session['carrito'] = {}
        self._save_cart()
        
    def get_items(self):
        """Obtener todos los items del carrito con su información completa"""
        carrito = self._get_cart()
        items = []
        total = 0
        
        if not self.producto_repo:
            return items, total
            
        for producto_id_str, cantidad in carrito.items():
            producto = self.producto_repo.get_by_id(int(producto_id_str))
            if producto:
                subtotal = float(producto.precio) * cantidad
                total += subtotal
                items.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
                
        return items, total
        
    def get_count(self):
        """Obtener cantidad total de items"""
        return sum(self._get_cart().values())
