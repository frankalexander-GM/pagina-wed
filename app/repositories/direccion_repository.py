from sqlalchemy.exc import SQLAlchemyError
from app.repositories.base_repository import BaseRepository
from app.models.ecommerce import Direccion

class DireccionRepository(BaseRepository):
    """
    Repositorio específico para Direcciones de envío
    """
    
    def __init__(self, session):
        """Inicializar repositorio de direcciones"""
        super().__init__(Direccion, session)
    
    def get_by_usuario(self, usuario_id):
        """Obtener todas las direcciones de un usuario"""
        try:
            return self.session.query(Direccion).filter_by(id_usuario=usuario_id).order_by(Direccion.fecha_creacion.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener direcciones del usuario: {e}")
            return []
    
    def set_default(self, usuario_id, id_direccion):
        """
        Establecer una dirección como predeterminada (si tuviéramos ese campo)
        Por ahora solo es un stub para futura funcionalidad.
        """
        pass
