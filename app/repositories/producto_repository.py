from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_
from app.repositories.base_repository import BaseRepository
from app.models.producto import Producto, HistorialStock

class ProductoRepository(BaseRepository):
    """
    Repositorio específico para productos
    Extiende BaseRepository con operaciones personalizadas
    """
    
    def __init__(self, session):
        """Inicializar repositorio de productos"""
        super().__init__(Producto, session)
    
    def get_by_artista(self, artista_id, disponibles_only=True, limit=None, offset=None):
        """
        Obtener productos de un artista
        
        Args:
            artista_id (int): ID del artista
            disponibles_only (bool): Solo productos con stock
            limit (int): Límite de resultados
            offset (int): Desplazamiento
            
        Returns:
            list: Lista de productos del artista
        """
        try:
            query = self.session.query(Producto).filter_by(id_artista=artista_id)
            
            if disponibles_only:
                query = query.filter(Producto.stock > 0)
            
            query = query.order_by(Producto.nombre)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener productos del artista: {e}")
            return []
    
    def get_disponibles(self, limit=None, offset=None):
        """
        Obtener productos disponibles (con stock)
        
        Args:
            limit (int): Límite de resultados
            offset (int): Desplazamiento
            
        Returns:
            list: Lista de productos disponibles
        """
        try:
            query = self.session.query(Producto).filter(Producto.stock > 0).order_by(Producto.nombre)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener productos disponibles: {e}")
            return []
    
    def get_agotados(self, limit=None, offset=None):
        """
        Obtener productos agotados
        
        Args:
            limit (int): Límite de resultados
            offset (int): Desplazamiento
            
        Returns:
            list: Lista de productos agotados
        """
        try:
            query = self.session.query(Producto).filter(Producto.stock == 0).order_by(Producto.nombre)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener productos agotados: {e}")
            return []
    
    def buscar_productos(self, termino, disponibles_only=True, limit=None):
        """
        Buscar productos por nombre o descripción
        
        Args:
            termino (str): Término de búsqueda
            disponibles_only (bool): Solo productos con stock
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de productos que coinciden con la búsqueda
        """
        try:
            query = self.session.query(Producto).filter(
                or_(
                    Producto.nombre.contains(termino),
                    Producto.descripcion.contains(termino)
                )
            )
            
            if disponibles_only:
                query = query.filter(Producto.stock > 0)
            
            query = query.order_by(Producto.nombre)
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al buscar productos: {e}")
            return []
    
    def actualizar_stock(self, producto_id, cantidad, motivo=None, usuario_id=None):
        """
        Actualizar stock de un producto
        
        Args:
            producto_id (int): ID del producto
            cantidad (int): Cantidad a agregar (positivo) o reducir (negativo)
            motivo (str): Motivo del cambio
            usuario_id (int): ID del usuario que realiza la acción
            
        Returns:
            Producto: Producto actualizado o None si hay error
        """
        try:
            producto = self.get_by_id(producto_id)
            if producto:
                stock_anterior = producto.stock
                nuevo_stock = stock_anterior + cantidad
                
                if nuevo_stock < 0:
                    print(f"Error: Stock negativo para producto {producto_id}")
                    return None
                
                # Actualizar stock
                actualizado = self.update(producto_id, {'stock': nuevo_stock}, usuario_id)
                
                if actualizado:
                    # Crear registro en historial
                    historial = HistorialStock(
                        id_producto=producto_id,
                        cambio=cantidad,
                        stock_anterior=stock_anterior,
                        stock_actual=nuevo_stock,
                        motivo=motivo or f"Actualización manual por usuario {usuario_id}"
                    )
                    self.session.add(historial)
                
                return actualizado
            return None
        except SQLAlchemyError as e:
            print(f"Error al actualizar stock: {e}")
            return None
    
    def reducir_stock_venta(self, producto_id, cantidad):
        """
        Reducir stock por venta
        
        Args:
            producto_id (int): ID del producto
            cantidad (int): Cantidad a reducir
            
        Returns:
            bool: True si se redujo correctamente, False si no hay stock suficiente
        """
        try:
            producto = self.get_by_id(producto_id)
            if producto and producto.stock >= cantidad:
                return self.actualizar_stock(
                    producto_id, 
                    -cantidad, 
                    f"Venta de {cantidad} unidades"
                ) is not None
            return False
        except SQLAlchemyError as e:
            print(f"Error al reducir stock por venta: {e}")
            return False
    
    def get_historial_stock(self, producto_id, limit=None):
        """
        Obtener historial de cambios de stock de un producto
        
        Args:
            producto_id (int): ID del producto
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de registros de historial
        """
        try:
            query = self.session.query(HistorialStock).filter_by(
                id_producto=producto_id
            ).order_by(HistorialStock.fecha.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener historial de stock: {e}")
            return []
    
    def get_mas_vendidos(self, limit=None):
        """
        Obtener productos más vendidos
        
        Args:
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de productos más vendidos
        """
        try:
            from app.models.ecommerce import OrdenItem
            from sqlalchemy import func, desc
            
            query = self.session.query(
                Producto,
                func.sum(OrdenItem.cantidad).label('total_vendido')
            ).join(
                OrdenItem, Producto.id_producto == OrdenItem.id_producto
            ).group_by(
                Producto.id_producto
            ).order_by(
                desc('total_vendido')
            )
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener productos más vendidos: {e}")
            return []
    
    def get_count_by_artista(self, artista_id, disponibles_only=True):
        """
        Obtener cantidad de productos de un artista
        
        Args:
            artista_id (int): ID del artista
            disponibles_only (bool): Solo productos con stock
            
        Returns:
            int: Cantidad de productos
        """
        try:
            query = self.session.query(Producto).filter_by(id_artista=artista_id)
            
            if disponibles_only:
                query = query.filter(Producto.stock > 0)
            
            return query.count()
        except SQLAlchemyError as e:
            print(f"Error al contar productos del artista: {e}")
            return 0
    
    def get_precio_range(self, artista_id=None):
        """
        Obtener rango de precios
        
        Args:
            artista_id (int): ID del artista (opcional)
            
        Returns:
            tuple: (precio_min, precio_max)
        """
        try:
            query = self.session.query(
                func.min(Producto.precio).label('min_precio'),
                func.max(Producto.precio).label('max_precio')
            )
            
            if artista_id:
                query = query.filter_by(id_artista=artista_id)
            
            result = query.first()
            return (float(result.min_precio) if result.min_precio else 0,
                   float(result.max_precio) if result.max_precio else 0)
        except SQLAlchemyError as e:
            print(f"Error al obtener rango de precios: {e}")
            return (0, 0)
