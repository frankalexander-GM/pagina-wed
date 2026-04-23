from datetime import datetime
from app.factories.app_factory import db

class Categoria(db.Model):
    """
    Modelo de Categoría basado en el script de base de datos
    Tabla: categorias
    """
    __tablename__ = 'categorias'
    
    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    obras = db.relationship('Obra', backref='categoria', lazy='dynamic')
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'
    
    def to_dict(self):
        """Convertir categoría a diccionario para API responses"""
        return {
            'id_categoria': self.id_categoria,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'obras_count': self.obras.count()
        }
    
    def get_obras_count(self):
        """Obtener cantidad de obras en esta categoría"""
        return self.obras.filter_by(visible=True).count()
    
    @staticmethod
    def get_all_with_counts():
        """Obtener todas las categorías con conteo de obras"""
        from sqlalchemy import func
        
        result = db.session.query(
            Categoria,
            func.count(Obra.id_obra).label('obras_count')
        ).outerjoin(
            Obra, 
            (Categoria.id_categoria == Obra.id_categoria) & (Obra.visible == True)
        ).group_by(Categoria.id_categoria).all()
        
        return result
