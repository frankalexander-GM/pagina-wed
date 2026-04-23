"""
Servicio de administración
Maneja operaciones de negocio específicas para administradores
"""

from datetime import datetime, timedelta
from sqlalchemy import func, text

class AdminService:
    """
    Servicio de administración para operaciones de negocio
    """
    
    def __init__(self, session):
        """
        Inicializar servicio de administración
        
        Args:
            session: Sesión de base de datos
        """
        self.session = session
    
    def get_estadisticas_generales(self):
        """
        Obtener estadísticas generales del sistema
        
        Returns:
            dict: Estadísticas generales
        """
        from app.models.usuario import Usuario
        from app.models.obra import Obra
        from app.models.producto import Producto
        from app.models.categoria import Categoria
        
        try:
            # Estadísticas de usuarios
            total_usuarios = self.session.query(Usuario).count()
            usuarios_activos = self.session.query(Usuario).filter_by(estado='activo').count()
            artistas_activos = self.session.query(Usuario).filter_by(rol='artista', estado='activo').count()
            clientes_activos = self.session.query(Usuario).filter_by(rol='cliente', estado='activo').count()
            
            # Estadísticas de obras
            total_obras = self.session.query(Obra).count()
            obras_visibles = self.session.query(Obra).filter_by(visible=True).count()
            
            # Estadísticas de productos
            total_productos = self.session.query(Producto).count()
            productos_disponibles = self.session.query(Producto).filter(Producto.stock > 0).count()
            
            # Estadísticas de categorías
            total_categorias = self.session.query(Categoria).count()
            
            # Usuarios nuevos en último mes
            fecha_mes = datetime.utcnow() - timedelta(days=30)
            usuarios_nuevos = self.session.query(Usuario).filter(Usuario.fecha_registro >= fecha_mes).count()
            
            # Obras nuevas en último mes
            obras_nuevas = self.session.query(Obra).filter(Obra.fecha_publicacion >= fecha_mes).count()
            
            return {
                'usuarios': {
                    'total': total_usuarios,
                    'activos': usuarios_activos,
                    'artistas': artistas_activos,
                    'clientes': clientes_activos,
                    'nuevos_mes': usuarios_nuevas
                },
                'obras': {
                    'total': total_obras,
                    'visibles': obras_visibles,
                    'ocultas': total_obras - obras_visibles,
                    'nuevas_mes': obras_nuevas
                },
                'productos': {
                    'total': total_productos,
                    'disponibles': productos_disponibles,
                    'agotados': total_productos - productos_disponibles
                },
                'categorias': {
                    'total': total_categorias
                }
            }
        except Exception as e:
            print(f"Error al obtener estadísticas generales: {e}")
            return {}
    
    def get_usuarios_por_rol(self):
        """
        Obtener distribución de usuarios por rol
        
        Returns:
            list: Lista de diccionarios con rol y cantidad
        """
        from app.models.usuario import Usuario
        
        try:
            resultado = self.session.query(
                Usuario.rol,
                func.count(Usuario.id_usuario).label('cantidad')
            ).group_by(Usuario.rol).all()
            
            return [
                {'rol': row.rol, 'cantidad': row.cantidad}
                for row in resultado
            ]
        except Exception as e:
            print(f"Error al obtener usuarios por rol: {e}")
            return []
    
    def get_obras_por_categoria(self):
        """
        Obtener distribución de obras por categoría
        
        Returns:
            list: Lista de diccionarios con categoría y cantidad
        """
        from app.models.obra import Obra
        from app.models.categoria import Categoria
        
        try:
            resultado = self.session.query(
                Categoria.nombre,
                func.count(Obra.id_obra).label('cantidad')
            ).join(
                Obra, Categoria.id_categoria == Obra.id_categoria
            ).filter(
                Obra.visible == True
            ).group_by(
                Categoria.id_categoria, Categoria.nombre
            ).order_by(
                func.count(Obra.id_obra).desc()
            ).all()
            
            return [
                {'categoria': row.nombre, 'cantidad': row.cantidad}
                for row in resultado
            ]
        except Exception as e:
            print(f"Error al obtener obras por categoría: {e}")
            return []
    
    def get_auditoria_registros(self, tabla=None, accion=None, limit=None):
        """
        Obtener registros de auditoría con filtros
        
        Args:
            tabla (str): Filtrar por tabla
            accion (str): Filtrar por acción
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de registros de auditoría
        """
        from app.models.auditoria import Auditoria
        
        try:
            query = self.session.query(Auditoria)
            
            if tabla:
                query = query.filter(Auditoria.tabla_afectada == tabla)
            
            if accion:
                query = query.filter(Auditoria.accion == accion)
            
            query = query.order_by(Auditoria.fecha.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            print(f"Error al obtener registros de auditoría: {e}")
            return []
    
    def get_estadisticas_mensuales(self, meses=6):
        """
        Obtener estadísticas mensuales de los últimos N meses
        
        Args:
            meses (int): Número de meses hacia atrás
            
        Returns:
            list: Lista de estadísticas mensuales
        """
        from app.models.usuario import Usuario
        from app.models.obra import Obra
        
        try:
            estadisticas = []
            
            for i in range(meses):
                fecha_inicio = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
                fecha_fin = (fecha_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                
                # Usuarios registrados en el mes
                usuarios_mes = self.session.query(Usuario).filter(
                    Usuario.fecha_registro >= fecha_inicio,
                    Usuario.fecha_registro <= fecha_fin
                ).count()
                
                # Obras publicadas en el mes
                obras_mes = self.session.query(Obra).filter(
                    Obra.fecha_publicacion >= fecha_inicio,
                    Obra.fecha_publicacion <= fecha_fin
                ).count()
                
                estadisticas.append({
                    'mes': fecha_inicio.strftime('%Y-%m'),
                    'usuarios_registrados': usuarios_mes,
                    'obras_publicadas': obras_mes
                })
            
            return estadisticas[::-1]  # Ordenar del más antiguo al más reciente
        except Exception as e:
            print(f"Error al obtener estadísticas mensuales: {e}")
            return []
    
    def get_artistas_mas_productivos(self, limit=10):
        """
        Obtener artistas más productivos (con más obras)
        
        Args:
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de artistas con estadísticas
        """
        from app.models.usuario import Usuario
        from app.models.obra import Obra
        
        try:
            resultado = self.session.query(
                Usuario.id_usuario,
                Usuario.nombre,
                Usuario.username,
                func.count(Obra.id_obra).label('obras_count')
            ).join(
                Obra, Usuario.id_usuario == Obra.id_artista
            ).filter(
                Usuario.rol == 'artista',
                Usuario.estado == 'activo',
                Obra.visible == True
            ).group_by(
                Usuario.id_usuario, Usuario.nombre, Usuario.username
            ).order_by(
                func.count(Obra.id_obra).desc()
            ).limit(limit).all()
            
            return [
                {
                    'id_usuario': row.id_usuario,
                    'nombre': row.nombre,
                    'username': row.username,
                    'obras_count': row.obras_count
                }
                for row in resultado
            ]
        except Exception as e:
            print(f"Error al obtener artistas más productivos: {e}")
            return []
    
    def get_categorias_mas_populares(self, limit=10):
        """
        Obtener categorías más populares (con más obras)
        
        Args:
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de categorías con estadísticas
        """
        from app.models.categoria import Categoria
        from app.models.obra import Obra
        
        try:
            resultado = self.session.query(
                Categoria.id_categoria,
                Categoria.nombre,
                func.count(Obra.id_obra).label('obras_count'),
                func.count(func.distinct(Obra.id_artista)).label('artistas_count')
            ).join(
                Obra, Categoria.id_categoria == Obra.id_categoria
            ).filter(
                Obra.visible == True
            ).group_by(
                Categoria.id_categoria, Categoria.nombre
            ).order_by(
                func.count(Obra.id_obra).desc()
            ).limit(limit).all()
            
            return [
                {
                    'id_categoria': row.id_categoria,
                    'nombre': row.nombre,
                    'obras_count': row.obras_count,
                    'artistas_count': row.artistas_count
                }
                for row in resultado
            ]
        except Exception as e:
            print(f"Error al obtener categorías más populares: {e}")
            return []
    
    def get_actividad_reciente(self, dias=7):
        """
        Obtener actividad reciente del sistema
        
        Args:
            dias (int): Días hacia atrás
            
        Returns:
            dict: Actividad reciente por tipo
        """
        from app.models.usuario import Usuario
        from app.models.obra import Obra
        from app.models.producto import Producto
        from app.models.auditoria import Auditoria
        
        try:
            fecha_limite = datetime.utcnow() - timedelta(days=dias)
            
            # Usuarios nuevos
            usuarios_nuevos = self.session.query(Usuario).filter(
                Usuario.fecha_registro >= fecha_limite
            ).count()
            
            # Obras nuevas
            obras_nuevas = self.session.query(Obra).filter(
                Obra.fecha_publicacion >= fecha_limite
            ).count()
            
            # Productos nuevos
            productos_nuevos = self.session.query(Producto).filter(
                Producto.fecha_creacion >= fecha_limite
            ).count()
            
            # Cambios en el sistema (auditoría)
            cambios_sistema = self.session.query(Auditoria).filter(
                Auditoria.fecha >= fecha_limite
            ).count()
            
            return {
                'usuarios_nuevos': usuarios_nuevos,
                'obras_nuevas': obras_nuevas,
                'productos_nuevos': productos_nuevos,
                'cambios_sistema': cambios_sistema,
                'periodo_dias': dias
            }
        except Exception as e:
            print(f"Error al obtener actividad reciente: {e}")
            return {}
    
    def get_reporte_usuarios(self, rol=None, estado=None, limit=None):
        """
        Obtener reporte de usuarios con filtros
        
        Args:
            rol (str): Filtrar por rol
            estado (str): Filtrar por estado
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de usuarios con estadísticas
        """
        from app.models.usuario import Usuario
        from app.models.obra import Obra
        
        try:
            query = self.session.query(Usuario)
            
            if rol:
                query = query.filter(Usuario.rol == rol)
            
            if estado:
                query = query.filter(Usuario.estado == estado)
            
            usuarios = query.limit(limit).all() if limit else query.all()
            
            reporte = []
            for usuario in usuarios:
                # Estadísticas por usuario
                if usuario.rol == 'artista':
                    obras_count = self.session.query(Obra).filter(
                        Obra.id_artista == usuario.id_usuario,
                        Obra.visible == True
                    ).count()
                else:
                    obras_count = 0
                
                reporte.append({
                    'id_usuario': usuario.id_usuario,
                    'nombre': usuario.nombre,
                    'username': usuario.username,
                    'email': usuario.email,
                    'rol': usuario.rol,
                    'estado': usuario.estado,
                    'fecha_registro': usuario.fecha_registro,
                    'obras_count': obras_count
                })
            
            return reporte
        except Exception as e:
            print(f"Error al obtener reporte de usuarios: {e}")
            return []
    
    def limpiar_auditoria_antigua(self, dias=90):
        """
        Limpiar registros de auditoría antiguos
        
        Args:
            dias (int): Días de antigüedad para eliminar
            
        Returns:
            tuple: (bool, int) - (exitoso, cantidad_eliminada)
        """
        from app.models.auditoria import Auditoria
        
        try:
            fecha_limite = datetime.utcnow() - timedelta(days=dias)
            
            cantidad_antes = self.session.query(Auditoria).count()
            
            # Eliminar registros antiguos
            self.session.query(Auditoria).filter(
                Auditoria.fecha < fecha_limite
            ).delete()
            
            self.session.commit()
            
            cantidad_despues = self.session.query(Auditoria).count()
            cantidad_eliminada = cantidad_antes - cantidad_despues
            
            return (True, cantidad_eliminada)
        except Exception as e:
            print(f"Error al limpiar auditoría antigua: {e}")
            self.session.rollback()
            return (False, 0)
