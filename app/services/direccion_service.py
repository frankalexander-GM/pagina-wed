"""
Servicio de gestión de Direcciones
"""

class DireccionService:
    """
    Servicio de direcciones para operaciones de negocio
    """
    
    def __init__(self, direccion_repository):
        self.direccion_repo = direccion_repository
        
    def get_by_usuario(self, usuario_id):
        """Obtener todas las direcciones de un usuario"""
        return self.direccion_repo.get_by_usuario(usuario_id)
        
    def get_by_id(self, id_direccion):
        """Obtener dirección por ID"""
        return self.direccion_repo.get_by_id(id_direccion)
        
    def agregar_direccion(self, data):
        """Agregar una nueva dirección"""
        direccion = self.direccion_repo.create(data)
        if direccion:
            self.direccion_repo.save()
            return True, direccion
        return False, None
        
    def actualizar_direccion(self, id_direccion, data):
        """Actualizar una dirección existente"""
        direccion = self.direccion_repo.update(id_direccion, data)
        if direccion:
            self.direccion_repo.save()
            return True, direccion
        return False, None
        
    def eliminar_direccion(self, id_direccion):
        """Eliminar una dirección"""
        if self.direccion_repo.delete(id_direccion):
            self.direccion_repo.save()
            return True
        return False
