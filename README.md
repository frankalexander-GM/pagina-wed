# Art Platform Backend

Backend completo para plataforma de arte con patrón de fábrica, SQLite y Flask.

## **Información del Proyecto**

### **Características Principales**
- **Arquitectura**: Patrón de Fábrica completo
- **Base de Datos**: SQLite (fácil instalación)
- **Autenticación**: Flask-Login con encriptación Bcrypt
- **Roles**: Admin, Artista, Cliente
- **API RESTful**: Endpoints completos para frontend
- **Templates HTML**: Bootstrap 5 listos para usar

### **Funcionalidades Implementadas**
- **Gestión de Usuarios**: Registro, login, perfiles, follows
- **Gestión de Obras**: CRUD, favoritos, visibilidad
- **Gestión de Productos**: E-commerce, stock, precios
- **Gestión de Categorías**: Organización de contenido
- **Panel de Administración**: Estadísticas, auditoría
- **Blog**: Entradas y comentarios
- **Moodboards**: Lienzos para clientes
- **Newsletters**: Sistema de comunicación

---

## **Instalación Rápida**

### **1. Crear Entorno Virtual**
```bash
# Navegar al directorio del proyecto
cd "c:\Users\mijaa\OneDrive\Escritorio\python\Proyecto plataforma\prototipo de la pagina"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### **2. Instalar Dependencias**
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### **3. Inicializar Base de Datos**
```bash
# Crear base de datos y datos iniciales
python init_db.py
```

### **4. Iniciar Aplicación**
```bash
# Iniciar servidor de desarrollo
python run.py
```

### **5. Acceder a la Aplicación**
- **URL Principal**: http://localhost:5000
- **Panel Admin**: http://localhost:5000/admin/dashboard
- **API Endpoints**: http://localhost:5000/api/

**Usuario Administrador por Defecto:**
- **Email**: admin@artplatform.com
- **Password**: admin123

---

## **Estructura del Proyecto**

```
prototipo de la pagina/
|   run.py                    # Punto de entrada
|   init_db.py               # Script de inicialización
|   requirements.txt         # Dependencias
|   
|   app/
|   |   __init__.py
|   |   config/              # Configuración por entorno
|   |   |   __init__.py
|   |   |   config.py
|   |   
|   |   factories/           # Patrón de fábrica
|   |   |   __init__.py
|   |   |   app_factory.py
|   |   |   db_factory.py
|   |   |   service_factory.py
|   |   
|   |   models/              # Modelos SQLAlchemy
|   |   |   __init__.py
|   |   |   usuario.py
|   |   |   obra.py
|   |   |   producto.py
|   |   |   categoria.py
|   |   |   blog.py
|   |   |   ecommerce.py
|   |   |   moodboard.py
|   |   |   newsletter.py
|   |   |   auditoria.py
|   |   
|   |   repositories/        # Repositorios de datos
|   |   |   __init__.py
|   |   |   base_repository.py
|   |   |   usuario_repository.py
|   |   |   obra_repository.py
|   |   |   producto_repository.py
|   |   |   categoria_repository.py
|   |   
|   |   services/             # Lógica de negocio
|   |   |   __init__.py
|   |   |   auth_service.py
|   |   |   usuario_service.py
|   |   |   obra_service.py
|   |   |   producto_service.py
|   |   |   categoria_service.py
|   |   |   admin_service.py
|   |   
|   |   controllers/         # Controladores/Blueprints
|   |   |   __init__.py
|   |   |   auth.py
|   |   |   public.py
|   |   |   artista.py
|   |   |   cliente.py
|   |   |   admin.py
|   |   |   api.py
|   |   
|   |   templates/           # Templates HTML
|   |   |   base.html
|   |   |   auth/
|   |   |   public/
|   |   |   artista/
|   |   |   cliente/
|   |   |   admin/
|   |   |   errors/
|   |   
|   |   static/              # Archivos estáticos
|   |   |   css/
|   |   |   js/
|   |   |   uploads/
```

---

## **API Endpoints Principales**

### **Autenticación**
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrar usuario
- `POST /auth/logout` - Cerrar sesión

### **Públicos**
- `GET /api/obras` - Listar obras públicas
- `GET /api/artistas` - Listar artistas
- `GET /api/categorias` - Listar categorías

### **Privados (requieren autenticación)**
- `GET /api/usuario/perfil` - Perfil del usuario
- `POST /api/usuario/favoritos/obras/{id}` - Agregar favorito
- `POST /api/usuario/seguir-artista/{id}` - Seguir artista

### **Administración**
- `GET /api/estadisticas/usuarios-por-rol` - Estadísticas por rol
- `GET /api/estadisticas/obras-por-categoria` - Obras por categoría

---

## **Configuración**

### **Variables de Entorno**
```bash
# Entorno de ejecución
FLASK_ENV=development

# Clave secreta (cambiar en producción)
SECRET_KEY=tu-clave-secreta-aqui

# URL de base de datos (opcional, usa SQLite por defecto)
DATABASE_URL=sqlite:///art_platform.db
```

### **Configuración por Entorno**
- **Development**: Debug activado, SQLite local
- **Testing**: Base de datos en memoria
- **Production**: Debug desactivado, seguridad reforzada

---

## **Desarrollo**

### **Comandos Útiles**
```bash
# Activar entorno virtual
venv\Scripts\activate

# Instalar nuevas dependencias
pip install nombre-paquete
pip freeze > requirements.txt

# Reinicializar base de datos
python init_db.py

# Ejecutar en modo desarrollo
python run.py

# Ejecutar en modo producción
export FLASK_ENV=production
python run.py
```

### **Estructura de Datos**
La base de datos incluye:
- **Usuarios**: Admin, Artista, Cliente
- **Obras**: Arte con categorías y favoritos
- **Productos**: E-commerce con stock
- **Categorías**: Organización de contenido
- **Blog**: Entradas y comentarios
- **E-commerce**: Órdenes, pagos, direcciones
- **Moodboards**: Lienzos personalizados
- **Newsletters**: Comunicación masiva
- **Auditoría**: Registro de cambios

---

## **Producción**

### **Consideraciones de Seguridad**
1. **Cambiar SECRET_KEY** en producción
2. **Usar HTTPS** con certificado SSL
3. **Configurar firewall** adecuado
4. **Hacer backup** regular de la base de datos
5. **Monitorear logs** de errores
6. **Actualizar dependencias** regularmente

### **Despliegue Recomendado**
```bash
# Instalar servidor WSGI
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app.factories.app_factory:create_app('production')"
```

---

## **Troubleshooting**

### **Problemas Comunes**

**Error: ModuleNotFoundError**
```bash
# Asegurarse de que el entorno virtual está activado
venv\Scripts\activate
# Reinstalar dependencias
pip install -r requirements.txt
```

**Error: Base de datos no encontrada**
```bash
# Inicializar base de datos
python init_db.py
```

**Error: Permiso denegado**
```bash
# Ejecutar como administrador o verificar permisos de carpeta
```

---

## **Contribución**

### **Flujo de Trabajo**
1. Crear rama para nueva funcionalidad
2. Implementar cambios
3. Probar exhaustivamente
4. Hacer commit con mensaje descriptivo
5. Hacer push y crear Pull Request

### **Estándares de Código**
- Usar Python 3.8+
- Seguir PEP 8
- Documentar funciones y clases
- Escribir pruebas unitarias
- Mantener compatibilidad con SQLite

---

## **Licencia**

Este proyecto es para uso educativo y desarrollo.

---

## **Soporte**

Para soporte técnico:
1. Revisar sección de Troubleshooting
2. Verificar logs de la aplicación
3. Revisar configuración del entorno
4. Consultar documentación de Flask y SQLAlchemy

---

**¡El backend está listo para usar!**