from app.models.ecommerce import Orden
from sqlalchemy import desc

class OrdenService:
    def __init__(self, session=None):
        self.session = session
        
    def crear_orden(self, data):
        # Stub for MVP creation
        return None
        
    def get_by_usuario(self, usuario_id):
        """Obtener historial de órdenes de un usuario"""
        return self.session.query(Orden).filter_by(id_cliente=usuario_id).order_by(desc(Orden.fecha_creacion)).all()
        
    def get_count_by_usuario(self, usuario_id):
        """Obtener cantidad de órdenes de un usuario"""
        return self.session.query(Orden).filter_by(id_cliente=usuario_id).count()
