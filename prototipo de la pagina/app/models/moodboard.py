from datetime import datetime
from app.factories.app_factory import db

class Lienzo(db.Model):
    """
    Modelo de Lienzo/Moodboard basado en el script de base de datos
    Tabla: lienzos
    """
    __tablename__ = 'lienzos'
    
    id_lienzo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('LienzoItem', backref='lienzo', lazy='dynamic',
                          cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lienzo {self.nombre}>'
    
    def to_dict(self):
        """Convertir lienzo a diccionario para API responses"""
        return {
            'id_lienzo': self.id_lienzo,
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'items_count': self.items.count(),
            'obras': [item.obra.to_dict() for item in self.items]
        }
    
    def get_obras_count(self):
        """Obtener cantidad de obras en el lienzo"""
        return self.items.count()
    
    def agregar_obra(self, obra, nota=None):
        """Agregar una obra al lienzo"""
        # Verificar si la obra ya está en el lienzo
        if not self.items.filter_by(id_obra=obra.id_obra).first():
            item = LienzoItem(
                id_lienzo=self.id_lienzo,
                id_obra=obra.id_obra,
                nota=nota
            )
            db.session.add(item)
            return True
        return False
    
    def quitar_obra(self, obra):
        """Quitar una obra del lienzo"""
        item = self.items.filter_by(id_obra=obra.id_obra).first()
        if item:
            db.session.delete(item)
            return True
        return False

class LienzoItem(db.Model):
    """
    Modelo de Item de Lienzo basado en el script de base de datos
    Tabla: lienzo_items
    """
    __tablename__ = 'lienzo_items'
    
    id_lienzo = db.Column(db.Integer, db.ForeignKey('lienzos.id_lienzo'), primary_key=True)
    id_obra = db.Column(db.Integer, db.ForeignKey('obras.id_obra'), primary_key=True)
    nota = db.Column(db.Text)
    
    def __repr__(self):
        return f'<LienzoItem Lienzo:{self.id_lienzo} Obra:{self.id_obra}>'
    
    def to_dict(self):
        """Convertir item a diccionario para API responses"""
        return {
            'id_lienzo': self.id_lienzo,
            'id_obra': self.id_obra,
            'nota': self.nota,
            'obra': self.obra.to_dict() if self.obra else None
        }
