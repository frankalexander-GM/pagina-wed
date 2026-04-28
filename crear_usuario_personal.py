#!/usr/bin/env python3
"""
Script para crear un usuario administrador para el usuario.
"""
from app.factories.app_factory import create_app, db
from app.factories.service_factory import get_service_factory

app = create_app('development')

with app.app_context():
    service_factory = get_service_factory()
    usuario_repo   = service_factory.get_usuario_repository()
    auth_service   = service_factory.get_auth_service()

    usuarios_a_crear = [
        {
            'nombre':    'Frank Alexander',
            'username':  'frank',
            'email':     'frank@moly.com',
            'password':  'admin123',
            'rol':       'admin',
            'biografia': 'Administrador principal de la plataforma.',
            'estado':    'activo'
        }
    ]

    for datos in usuarios_a_crear:
        existente = usuario_repo.get_by_email(datos['email'])
        if existente:
            print(f"Ya existe una cuenta con el email: {datos['email']}")
            # Actualizar contraseña por si acaso
            existente_username = usuario_repo.get_by_username(datos['username'])
            if existente_username:
                print(f"Usuario {datos['username']} ya existe. Intentando resetear...")
            continue

        exitoso, usuario, errores = auth_service.registrar_usuario(datos)

        if exitoso:
            print(f"Cuenta creada exitosamente para {datos['nombre']}")
            print(f"Username: {datos['username']}")
            print(f"Email: {datos['email']}")
            print(f"Password: {datos['password']}")
        else:
            print(f"Error al crear cuenta: {errores}")
