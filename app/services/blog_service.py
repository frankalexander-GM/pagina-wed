"""
Servicio de blog
Maneja operaciones de entradas de blog de artistas
"""


class BlogService:
    """
    Servicio de blog para operaciones de negocio
    """
    
    def __init__(self, user_repo=None):
        self.user_repo = user_repo
    
    def get_entradas_artista(self, artista_id, limit=None):
        """Obtener entradas de blog de un artista"""
        from app.models.blog import EntradaBlog
        from app.factories.app_factory import db
        
        try:
            query = db.session.query(EntradaBlog).filter_by(
                id_artista=artista_id, visible=True
            ).order_by(EntradaBlog.fecha_publicacion.desc())
            if limit:
                query = query.limit(limit)
            return query.all()
        except Exception as e:
            print(f"Error al obtener entradas de blog: {e}")
            return []
    
    def get_entrada_by_id(self, entrada_id):
        """Obtener entrada de blog por ID"""
        from app.models.blog import EntradaBlog
        from app.factories.app_factory import db
        
        try:
            return db.session.query(EntradaBlog).filter_by(id_entrada=entrada_id).first()
        except Exception as e:
            print(f"Error al obtener entrada: {e}")
            return None
    
    def crear_entrada(self, data):
        """Crear nueva entrada de blog"""
        from app.models.blog import EntradaBlog
        from app.factories.app_factory import db
        
        try:
            entrada = EntradaBlog(**data)
            db.session.add(entrada)
            db.session.commit()
            return entrada
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear entrada: {e}")
            return None
