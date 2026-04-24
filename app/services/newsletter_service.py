"""
Servicio de newsletters
Maneja suscripciones y envío de newsletters
"""


class NewsletterService:
    """
    Servicio de newsletters para operaciones de negocio
    """
    
    def __init__(self, user_repo=None):
        self.user_repo = user_repo
    
    def suscribir(self, cliente_id, artista_id):
        """Suscribir un cliente al newsletter de un artista"""
        from app.models.newsletter import Suscripcion
        from app.factories.app_factory import db
        
        try:
            existente = db.session.query(Suscripcion).filter_by(
                id_cliente=cliente_id, id_artista=artista_id
            ).first()
            if existente:
                return False
            
            suscripcion = Suscripcion(id_cliente=cliente_id, id_artista=artista_id)
            db.session.add(suscripcion)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al suscribir: {e}")
            return False
    
    def desuscribir(self, cliente_id, artista_id):
        """Cancelar suscripción"""
        from app.models.newsletter import Suscripcion
        from app.factories.app_factory import db
        
        try:
            suscripcion = db.session.query(Suscripcion).filter_by(
                id_cliente=cliente_id, id_artista=artista_id
            ).first()
            if suscripcion:
                db.session.delete(suscripcion)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al desuscribir: {e}")
            return False
    
    def get_suscripciones_cliente(self, cliente_id):
        """Obtener suscripciones de un cliente"""
        from app.models.newsletter import Suscripcion
        from app.factories.app_factory import db
        
        try:
            return db.session.query(Suscripcion).filter_by(id_cliente=cliente_id).all()
        except Exception as e:
            print(f"Error al obtener suscripciones: {e}")
            return []
