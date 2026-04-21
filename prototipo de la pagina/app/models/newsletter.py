from datetime import datetime
from app.factories.app_factory import db

class Newsletter(db.Model):
    """
    Modelo de Newsletter basado en el script de base de datos
    Tabla: newsletters
    """
    __tablename__ = 'newsletters'
    
    id_newsletter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_artista = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    suscripciones = db.relationship('Usuario', secondary='bandeja_newsletter',
                                   lazy='subquery',
                                   backref=db.backref('newsletters_recibidos', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Newsletter {self.asunto}>'
    
    def to_dict(self):
        """Convertir newsletter a diccionario para API responses"""
        return {
            'id_newsletter': self.id_newsletter,
            'id_artista': self.id_artista,
            'asunto': self.asunto,
            'contenido': self.contenido,
            'fecha_envio': self.fecha_envio.isoformat() if self.fecha_envio else None,
            'artista_nombre': self.artista.nombre if self.artista else None,
            'suscriptores_count': len(self.suscripciones)
        }
    
    def get_suscriptores_count(self):
        """Obtener cantidad de suscriptores"""
        return len(self.suscripciones)
    
    def enviar_a_suscriptores(self, suscriptores_ids):
        """Enviar newsletter a suscriptores específicos"""
        for usuario_id in suscriptores_ids:
            # Agregar a la bandeja del suscriptor
            bandeja_entry = bandeja_newsletter.insert().values(
                id_usuario=usuario_id,
                id_newsletter=self.id_newsletter,
                leido=False
            )
            db.session.execute(bandeja_entry)

class Suscripcion(db.Model):
    """
    Modelo de Suscripción a Newsletter basado en el script de base de datos
    Tabla: suscripciones
    """
    __tablename__ = 'suscripciones'
    
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_artista = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cliente = db.relationship('Usuario', foreign_keys=[id_cliente], backref='suscripciones_hechas')
    artista = db.relationship('Usuario', foreign_keys=[id_artista], backref='suscriptores')
    
    def __repr__(self):
        return f'<Suscripcion Cliente:{self.id_cliente} Artista:{self.id_artista}>'
    
    def to_dict(self):
        """Convertir suscripción a diccionario para API responses"""
        return {
            'id_cliente': self.id_cliente,
            'id_artista': self.id_artista,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'cliente_nombre': self.cliente.nombre if self.cliente else None,
            'artista_nombre': self.artista.nombre if self.artista else None
        }

# Importar las tablas de relación desde usuario.py para evitar duplicación
from app.models.usuario import bandeja_newsletter
