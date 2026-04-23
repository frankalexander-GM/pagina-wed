#!/usr/bin/env python3
"""
Script para inicializar la base de datos SQLite
Crea todas las tablas necesarias para la plataforma de arte
"""

import os
from app.factories.app_factory import create_app, db
from app.factories.db_factory import DatabaseFactory

def init_database():
    """Inicializar la base de datos con todas las tablas"""
    
    # Crear aplicación Flask
    app = create_app('development')
    
    with app.app_context():
        print("Inicializando base de datos SQLite...")
        
        # Crear fábrica de base de datos
        db_factory = DatabaseFactory()
        
        # Obtener engine y session
        engine = db_factory.create_engine()
        session = db_factory.get_session()
        
        try:
            # Importar todos los modelos para que SQLAlchemy los reconozca
            from app.models import (
                Usuario, Categoria, Obra, Producto, 
                EntradaBlog, ComentarioBlog, Direccion, 
                Orden, OrdenItem, Pago, Lienzo, LienzoItem,
                Newsletter, Suscripcion, Auditoria
            )
            
            # Crear todas las tablas
            db.create_all()
            
            print("¡Base de datos inicializada exitosamente!")
            print(f"Base de datos creada en: {engine.url}")
            
            # Crear usuario administrador por defecto
            from app.services.auth_service import AuthService
            from app.factories.service_factory import get_service_factory
            
            service_factory = get_service_factory()
            usuario_repo = service_factory.get_usuario_repository()
            auth_service = AuthService(usuario_repo)
            
            # Verificar si ya existe un admin
            admin_existente = usuario_repo.get_by_email('admin@artplatform.com')
            
            if not admin_existente:
                # Crear usuario admin por defecto
                admin_data = {
                    'nombre': 'Administrador',
                    'username': 'admin',
                    'email': 'admin@artplatform.com',
                    'password': 'admin123',  # Cambiar en producción
                    'rol': 'admin',
                    'biografia': 'Administrador del sistema',
                    'estado': 'activo'
                }
                
                exitoso, admin_usuario, errores = auth_service.registrar_usuario(admin_data)
                
                if exitoso:
                    print("Usuario administrador creado exitosamente:")
                    print("  Email: admin@artplatform.com")
                    print("  Password: admin123")
                    print("  ¡IMPORTANTE! Cambiar esta contraseña en producción")
                else:
                    print("Error al crear usuario administrador:")
                    for error in errores:
                        print(f"  - {error}")
            else:
                print("Usuario administrador ya existe")
            
            # Crear algunas categorías de ejemplo
            categoria_repo = service_factory.get_categoria_repository()
            
            categorias_ejemplo = [
                {'nombre': 'Pintura', 'descripcion': 'Obras de pintura al óleo, acrílico, acuarela, etc.'},
                {'nombre': 'Escultura', 'descripcion': 'Obras escultóricas en diversos materiales'},
                {'nombre': 'Fotografía', 'descripcion': 'Arte fotográfico digital y analógico'},
                {'nombre': 'Arte Digital', 'descripcion': 'Ilustraciones digitales, arte NFT, etc.'},
                {'nombre': 'Dibujo', 'descripcion': 'Bocetos, ilustraciones, dibujos técnicos'}
            ]
            
            for cat_data in categorias_ejemplo:
                if not categoria_repo.name_exists(cat_data['nombre']):
                    categoria = categoria_repo.create(cat_data)
                    print(f"Categoría creada: {cat_data['nombre']}")
                else:
                    print(f"Categoría ya existe: {cat_data['nombre']}")
            
            # Guardar cambios
            session.commit()
            
            print("\n¡Inicialización completada!")
            print("La base de datos está lista para usar.")
            
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            session.rollback()
            raise
        finally:
            session.close()

if __name__ == '__main__':
    init_database()
