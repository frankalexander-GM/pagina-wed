"""
Servicio de gestión de categorías
Maneja operaciones de negocio relacionadas con categorías de obras
"""

class CategoriaService:
    """
    Servicio de categorías para operaciones de negocio
    """
    
    def __init__(self, categoria_repository):
        """
        Inicializar servicio de categorías
        
        Args:
            categoria_repository: Repositorio de categorías
        """
        self.categoria_repo = categoria_repository
    
    def get_by_id(self, categoria_id):
        """
        Obtener categoría por ID
        
        Args:
            categoria_id (int): ID de la categoría
            
        Returns:
            Categoria: Instancia de la categoría o None
        """
        return self.categoria_repo.get_by_id(categoria_id)
    
    def get_all(self, limit=None, offset=None):
        """
        Obtener todas las categorías
        
        Args:
            limit (int): Límite de resultados
            offset (int): Desplazamiento
            
        Returns:
            list: Lista de categorías
        """
        return self.categoria_repo.get_all(limit=limit, offset=offset)
    
    def get_all_with_obras_count(self):
        """
        Obtener todas las categorías con conteo de obras
        
        Returns:
            list: Lista de tuplas (Categoria, obras_count)
        """
        return self.categoria_repo.get_all_with_obras_count()
    
    def get_by_name(self, nombre):
        """
        Obtener categoría por nombre
        
        Args:
            nombre (str): Nombre de la categoría
            
        Returns:
            Categoria: Instancia de la categoría o None
        """
        return self.categoria_repo.get_by_name(nombre)
    
    def name_exists(self, nombre, exclude_id=None):
        """
        Verificar si nombre de categoría ya existe
        
        Args:
            nombre (str): Nombre a verificar
            exclude_id (int): ID a excluir de la verificación
            
        Returns:
            bool: True si existe, False si no
        """
        return self.categoria_repo.name_exists(nombre, exclude_id)
    
    def get_with_obras(self, categoria_id, limit=None, offset=None):
        """
        Obtener categoría con sus obras
        
        Args:
            categoria_id (int): ID de la categoría
            limit (int): Límite de obras
            offset (int): Desplazamiento de obras
            
        Returns:
            tuple: (Categoria, obras_list)
        """
        return self.categoria_repo.get_with_obras(categoria_id, limit=limit, offset=offset)
    
    def get_populares(self, limit=None):
        """
        Obtener categorías más populares (con más obras)
        
        Args:
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de tuplas (Categoria, obras_count)
        """
        return self.categoria_repo.get_populares(limit=limit)
    
    def get_empty_categories(self):
        """
        Obtener categorías sin obras
        
        Returns:
            list: Lista de categorías sin obras
        """
        return self.categoria_repo.get_empty_categories()
    
    def buscar_categorias(self, termino, limit=None):
        """
        Buscar categorías por nombre o descripción
        
        Args:
            termino (str): Término de búsqueda
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de categorías que coinciden con la búsqueda
        """
        return self.categoria_repo.buscar_categorias(termino, limit=limit)
    
    def get_obras_count(self, categoria_id):
        """
        Obtener cantidad de obras en una categoría
        
        Args:
            categoria_id (int): ID de la categoría
            
        Returns:
            int: Cantidad de obras
        """
        return self.categoria_repo.get_obras_count(categoria_id)
    
    def get_artistas_count(self, categoria_id):
        """
        Obtener cantidad de artistas únicos en una categoría
        
        Args:
            categoria_id (int): ID de la categoría
            
        Returns:
            int: Cantidad de artistas únicos
        """
        return self.categoria_repo.get_artistas_count(categoria_id)
    
    def crear_categoria(self, data, usuario_id=None):
        """
        Crear nueva categoría
        
        Args:
            data (dict): Datos de la categoría
            usuario_id (int): ID del usuario que crea
            
        Returns:
            tuple: (bool, Categoria) - (exitoso, categoria_creada)
        """
        # Validar datos
        if not data.get('nombre', '').strip():
            return (False, None)
        
        # Verificar si ya existe
        if self.name_exists(data['nombre']):
            return (False, None)
        
        # Crear categoría
        categoria = self.categoria_repo.create(data)
        
        if categoria:
            self.categoria_repo.save()
            return (True, categoria)
        
        return (False, None)
    
    def actualizar_categoria(self, categoria_id, data, usuario_id=None):
        """
        Actualizar categoría existente
        
        Args:
            categoria_id (int): ID de la categoría
            data (dict): Datos a actualizar
            usuario_id (int): ID del usuario que actualiza
            
        Returns:
            tuple: (bool, Categoria) - (exitoso, categoria_actualizada)
        """
        # Validar datos
        if 'nombre' in data and not data['nombre'].strip():
            return (False, None)
        
        # Verificar si el nombre ya existe (excluyendo la categoría actual)
        if 'nombre' in data and self.name_exists(data['nombre'], exclude_id=categoria_id):
            return (False, None)
        
        # Actualizar categoría
        categoria_actualizada = self.categoria_repo.update_with_obras_count(categoria_id, data, usuario_id)
        
        if categoria_actualizada:
            self.categoria_repo.save()
            return (True, categoria_actualizada)
        
        return (False, None)
    
    def eliminar_categoria(self, categoria_id, usuario_id=None):
        """
        Eliminar categoría (solo si no tiene obras asociadas)
        
        Args:
            categoria_id (int): ID de la categoría
            usuario_id (int): ID del usuario que elimina
            
        Returns:
            tuple: (bool, str) - (exitoso, mensaje)
        """
        # Verificar si tiene obras asociadas
        obras_count = self.get_obras_count(categoria_id)
        
        if obras_count > 0:
            return (False, f'No se puede eliminar la categoría porque tiene {obras_count} obras asociadas')
        
        # Eliminar categoría
        exitoso = self.categoria_repo.delete(categoria_id, usuario_id)
        
        if exitoso:
            self.categoria_repo.save()
            return (True, 'Categoría eliminada correctamente')
        
        return (False, 'Error al eliminar la categoría')
    
    def count(self):
        """
        Contar total de categorías
        
        Returns:
            int: Cantidad de categorías
        """
        return self.categoria_repo.count()
    
    def get_estadisticas_generales(self):
        """
        Obtener estadísticas generales de categorías
        
        Returns:
            dict: Estadísticas generales
        """
        total_categorias = self.count()
        categorias_con_obras = len([cat for cat, count in self.get_all_with_obras_count() if count > 0])
        categorias_vacias = total_categorias - categorias_con_obras
        
        # Obtener la categoría con más obras
        populares = self.get_populares(limit=1)
        categoria_mas_popular = populares[0] if populares else None
        
        return {
            'total_categorias': total_categorias,
            'categorias_con_obras': categorias_con_obras,
            'categorias_vacias': categorias_vacias,
            'categoria_mas_popular': categoria_mas_popular
        }
    
    def get_categorias_con_estadisticas(self, limit=None):
        """
        Obtener categorías con estadísticas detalladas
        
        Args:
            limit (int): Límite de resultados
            
        Returns:
            list: Lista de categorías con estadísticas
        """
        categorias_data = self.get_all_with_obras_count()
        
        categorias_con_stats = []
        for categoria, obras_count in categorias_data:
            artistas_count = self.get_artistas_count(categoria.id_categoria)
            
            categoria_stats = {
                'categoria': categoria.to_dict(),
                'obras_count': obras_count,
                'artistas_count': artistas_count,
                'promedio_obras_por_artista': obras_count / artistas_count if artistas_count > 0 else 0
            }
            
            categorias_con_stats.append(categoria_stats)
        
        if limit:
            categorias_con_stats = categorias_con_stats[:limit]
        
        return categorias_con_stats
    
    def validar_categoria_data(self, data, exclude_id=None):
        """
        Validar datos de categoría
        
        Args:
            data (dict): Datos a validar
            exclude_id (int): ID a excluir de validación de unicidad
            
        Returns:
            tuple: (bool, list) - (es_valido, lista_errores)
        """
        errores = []
        
        # Validar nombre
        if not data.get('nombre', '').strip():
            errores.append('El nombre es obligatorio')
        elif len(data['nombre']) < 2:
            errores.append('El nombre debe tener al menos 2 caracteres')
        elif self.name_exists(data['nombre'], exclude_id):
            errores.append('El nombre de categoría ya existe')
        
        # Validar descripción (opcional)
        if 'descripcion' in data and len(data['descripcion']) > 500:
            errores.append('La descripción no puede exceder 500 caracteres')
        
        return (len(errores) == 0, errores)
    
    def get_categorias_para_select(self):
        """
        Obtener categorías en formato para select (id, nombre)
        
        Returns:
            list: Lista de diccionarios con id y nombre
        """
        categorias = self.get_all()
        
        return [
            {'id': cat.id_categoria, 'nombre': cat.nombre}
            for cat in categorias
        ]
    
    def actualizar_conteos_obras(self, categoria_id):
        """
        Actualizar conteos de obras para una categoría (si se usa caché)
        
        Args:
            categoria_id (int): ID de la categoría
            
        Returns:
            int: Nuevo conteo de obras
        """
        # Este método sería útil si implementamos caché de conteos
        return self.get_obras_count(categoria_id)
