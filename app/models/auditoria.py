from datetime import datetime
from app.factories.app_factory import db

class Auditoria(db.Model):
    """
    Modelo de Auditoría basado en el script de base de datos
    Tabla: auditoria
    """
    __tablename__ = 'auditoria'
    
    id_auditoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tabla_afectada = db.Column(db.String(50), nullable=False)
    id_registro = db.Column(db.Integer, nullable=False)
    accion = db.Column(db.String(20), nullable=False)  # INSERT, UPDATE, DELETE
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    usuario = db.relationship('Usuario', backref='auditorias_realizadas')
    
    def __repr__(self):
        return f'<Auditoria {self.accion} {self.tabla_afectada}:{self.id_registro}>'
    
    def to_dict(self):
        """Convertir auditoría a diccionario para API responses"""
        return {
            'id_auditoria': self.id_auditoria,
            'tabla_afectada': self.tabla_afectada,
            'id_registro': self.id_registro,
            'accion': self.accion,
            'id_usuario': self.id_usuario,
            'usuario_nombre': self.usuario.nombre if self.usuario else None,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
    
    @staticmethod
    def registrar_cambio(tabla, id_registro, accion, usuario_id=None, descripcion=None):
        """
        Registrar un cambio en la base de datos
        
        Args:
            tabla (str): Nombre de la tabla afectada
            id_registro (int): ID del registro afectado
            accion (str): Tipo de acción (INSERT, UPDATE, DELETE)
            usuario_id (int): ID del usuario que realizó la acción
            descripcion (str): Descripción del cambio
        """
        auditoria = Auditoria(
            tabla_afectada=tabla,
            id_registro=id_registro,
            accion=accion,
            id_usuario=usuario_id,
            descripcion=descripcion
        )
        db.session.add(auditoria)
        return auditoria
