"""
Servicio de órdenes de compra
Maneja la creación y gestión de órdenes
"""


class OrdenService:
    """
    Servicio de órdenes para operaciones de negocio
    """
    
    def __init__(self, user_repo=None, producto_repo=None):
        self.user_repo = user_repo
        self.producto_repo = producto_repo
    
    def crear_orden(self, cliente_id, direccion_id, items_carrito):
        """
        Crear una nueva orden desde el carrito
        
        Args:
            cliente_id (int): ID del cliente
            direccion_id (int): ID de la dirección de envío
            items_carrito (list): Items del carrito
            
        Returns:
            tuple: (bool, orden/None, mensaje)
        """
        from app.models.ecommerce import Orden, OrdenItem
        from app.factories.app_factory import db
        
        try:
            total = sum(item['precio'] * item['cantidad'] for item in items_carrito)
            
            orden = Orden(
                id_cliente=cliente_id,
                id_direccion=direccion_id,
                total=total,
                estado='pendiente'
            )
            db.session.add(orden)
            db.session.flush()
            
            for item in items_carrito:
                orden_item = OrdenItem(
                    id_orden=orden.id_orden,
                    id_producto=item['producto_id'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    subtotal=item['precio'] * item['cantidad']
                )
                db.session.add(orden_item)
                
                # Reducir stock
                if self.producto_repo:
                    self.producto_repo.reducir_stock_venta(item['producto_id'], item['cantidad'])
            
            db.session.commit()
            return (True, orden, 'Orden creada exitosamente')
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear orden: {e}")
            return (False, None, 'Error al crear la orden')
    
    def get_ordenes_cliente(self, cliente_id, limit=None):
        """Obtener órdenes de un cliente"""
        from app.models.ecommerce import Orden
        from app.factories.app_factory import db
        
        try:
            query = db.session.query(Orden).filter_by(id_cliente=cliente_id).order_by(Orden.fecha_creacion.desc())
            if limit:
                query = query.limit(limit)
            return query.all()
        except Exception as e:
            print(f"Error al obtener órdenes: {e}")
            return []
    
    def get_orden_by_id(self, orden_id):
        """Obtener orden por ID"""
        from app.models.ecommerce import Orden
        from app.factories.app_factory import db
        
        try:
            return db.session.query(Orden).filter_by(id_orden=orden_id).first()
        except Exception as e:
            print(f"Error al obtener orden: {e}")
            return None
