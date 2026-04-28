import os
import time
from sqlalchemy import text
from app.factories.app_factory import create_app, db
from app.models.categoria import Categoria
from app.factories.service_factory import get_service_factory

def seed_categories():
    app = create_app('development')
    with app.app_context():
        # Aumentar el timeout de SQLite para evitar bloqueos
        db.session.execute(text("PRAGMA busy_timeout = 30000"))
        
        service_factory = get_service_factory()
        categoria_service = service_factory.get_categoria_service()
        
        behance_categories = [
            {'nombre': 'Diseño Gráfico', 'descripcion': 'Diseño visual, layouts y comunicación gráfica.'},
            {'nombre': 'Fotografía', 'descripcion': 'Fotografía artística, comercial y documental.'},
            {'nombre': 'Ilustración', 'descripcion': 'Dibujo, pintura digital e ilustración tradicional.'},
            {'nombre': 'UI/UX', 'descripcion': 'Diseño de interfaces y experiencia de usuario.'},
            {'nombre': 'Motion Graphics', 'descripcion': 'Animación y gráficos en movimiento.'},
            {'nombre': 'Branding', 'descripcion': 'Identidad corporativa, logotipos y estrategia de marca.'},
            {'nombre': 'Dirección de Arte', 'descripcion': 'Concepto y dirección visual de proyectos creativos.'},
            {'nombre': 'Diseño de Producto', 'descripcion': 'Desarrollo de productos físicos e industriales.'},
            {'nombre': 'Moda', 'descripcion': 'Diseño de indumentaria, accesorios y estilismo.'},
            {'nombre': 'Arquitectura', 'descripcion': 'Diseño arquitectónico y urbanismo.'},
            {'nombre': 'Diseño de Interiores', 'descripcion': 'Diseño de espacios interiores y decoración.'},
            {'nombre': 'Arte Digital', 'descripcion': 'Creaciones artísticas mediante medios digitales.'},
            {'nombre': 'Diseño de Juegos', 'descripcion': 'Visuales y mecánicas para videojuegos.'},
            {'nombre': 'Tipografía', 'descripcion': 'Diseño de fuentes y letras personalizadas.'},
            {'nombre': 'Diseño Web', 'descripcion': 'Diseño de sitios y aplicaciones web.'},
            {'nombre': 'Diseño de Personajes', 'descripcion': 'Creación y desarrollo de personajes.'},
            {'nombre': 'Packaging', 'descripcion': 'Diseño de empaques y envases.'},
            {'nombre': 'Bellas Artes', 'descripcion': 'Disciplinas artísticas tradicionales.'},
            {'nombre': 'Animación', 'descripcion': 'Animación 2D, 3D y stop motion.'},
            {'nombre': 'Diseño Industrial', 'descripcion': 'Diseño de objetos para producción en serie.'},
            {'nombre': 'Artesanía', 'descripcion': 'Obras hechas a mano y técnicas artesanales.'},
            {'nombre': 'Arte Urbano', 'descripcion': 'Graffiti, muralismo y arte en espacios públicos.'}
        ]
        
        count = 0
        for cat_data in behance_categories:
            try:
                if not categoria_service.name_exists(cat_data['nombre']):
                    categoria_service.create(cat_data)
                    db.session.commit() # Commit uno por uno para asegurar el guardado
                    print(f"Agregada: {cat_data['nombre']}")
                    count += 1
                else:
                    print(f"Ya existe: {cat_data['nombre']}")
            except Exception as e:
                print(f"Error al agregar {cat_data['nombre']}: {e}")
                db.session.rollback()
                time.sleep(1) # Esperar un segundo antes de reintentar el siguiente
        
        print(f"\nSe han agregado {count} nuevas categorías inspiradas en Behance.")

if __name__ == '__main__':
    seed_categories()
