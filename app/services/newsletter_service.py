from app.models.newsletter import Newsletter, Suscripcion
from app.models.usuario import bandeja_newsletter
from sqlalchemy import desc

class NewsletterService:
    def __init__(self, session=None):
        self.session = session
        
    def get_by_usuario(self, usuario_id, limit=None):
        """Obtener newsletters recibidos por un usuario (Bandeja de Entrada)"""
        from app.models.usuario import bandeja_newsletter
        
        query = self.session.query(Newsletter).join(
            bandeja_newsletter, Newsletter.id_newsletter == bandeja_newsletter.c.id_newsletter
        ).filter(
            bandeja_newsletter.c.id_usuario == usuario_id
        ).order_by(desc(Newsletter.fecha_envio))
        
        if limit:
            query = query.limit(limit)
            
        return query.all()
        
    def suscribir(self, usuario_id, artista_id):
        """Suscribir un usuario a un artista"""
        # Verificar si ya existe
        existe = self.session.query(Suscripcion).filter_by(
            id_cliente=usuario_id, id_artista=artista_id
        ).first()
        
        if existe:
            return True
            
        suscripcion = Suscripcion(id_cliente=usuario_id, id_artista=artista_id)
        self.session.add(suscripcion)
        try:
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False
        
    def desuscribir(self, usuario_id, artista_id):
        """Desuscribir un usuario de un artista"""
        suscripcion = self.session.query(Suscripcion).filter_by(
            id_cliente=usuario_id, id_artista=artista_id
        ).first()
        
        if suscripcion:
            self.session.delete(suscripcion)
            try:
                self.session.commit()
                return True
            except Exception:
                self.session.rollback()
                return False
        return True
