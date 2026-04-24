#!/usr/bin/env python3
"""
Script para crear el usuario administrador de tu compañero.
"""
from app.factories.app_factory import create_app, db
from app.factories.service_factory import get_service_factory

app = create_app('development')

with app.app_context():
    service_factory = get_service_factory()
    usuario_repo   = service_factory.get_usuario_repository()
    auth_service   = service_factory.get_auth_service()

    admins_a_crear = [
        {
            'nombre':    'NOMBRE COMPAÑERO',
            'username':  'USERNAME_COMPAÑERO',
            'email':     'EMAIL_COMPAÑERO@gmail.com',
            'password':  'PASSWORD_SEGURO',
            'rol':       'admin',
            'biografia': 'Co-fundador y administrador de Ágora Art.',
            'estado':    'activo'
        }
    ]

    for datos in admins_a_crear:
        existente = usuario_repo.get_by_email(datos['email'])
        if existente:
            print(f"Ya existe una cuenta con el email: {datos['email']}")
            continue

        exitoso, usuario, errores = auth_service.registrar_usuario(datos)

        if exitoso:
            print(f"Cuenta creada exitosamente para {datos['nombre']}")
        else:
            print(f"Error al crear cuenta: {errores}")
