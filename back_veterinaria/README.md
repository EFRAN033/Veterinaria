# Veterinaria API - Backend

API REST desarrollada con FastAPI y PostgreSQL para sistema de gestión veterinaria.

## 🚀 Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para Python
- **Alembic**: Migraciones de base de datos
- **JWT**: Autenticación con tokens
- **Pydantic**: Validación de datos

## 📋 Requisitos

- Python 3.10+
- PostgreSQL 14+
- pip

## 🛠️ Instalación

1. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos:**
```bash
# Crear base de datos en PostgreSQL
createdb veterinaria

# O usando psql:
psql -U postgres
CREATE DATABASE veterinaria;
\q
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Ejecutar migraciones:**
```bash
alembic upgrade head
```

6. **Iniciar servidor:**
```bash
uvicorn app.main:app --reload --port 8000
```

## 📚 Documentación API

Una vez iniciado el servidor, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🗂️ Estructura del Proyecto

```
back_veterinaria/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Endpoints API
│   ├── dependencies/    # Dependencias (auth, db)
│   ├── utils/           # Utilidades
│   ├── config.py        # Configuración
│   ├── database.py      # Conexión DB
│   └── main.py          # App principal
├── alembic/             # Migraciones
├── tests/               # Tests
├── requirements.txt     # Dependencias
└── .env                 # Variables de entorno
```

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens) para autenticación.

**Endpoints de autenticación:**
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

## 📝 Endpoints Principales

### Servicios
- `GET /api/services` - Listar servicios
- `POST /api/services` - Crear servicio (admin)

### Citas
- `GET /api/appointments` - Listar citas
- `POST /api/appointments` - Crear cita

### Productos
- `GET /api/products` - Listar productos
- `POST /api/products` - Crear producto (admin)

### Adopciones
- `GET /api/adoptions` - Listar mascotas en adopción
- `POST /api/adoptions` - Crear listing (admin)

## 🧪 Testing

```bash
pytest
```

## 📦 Deployment

```bash
# Producción con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📄 Licencia

MIT
