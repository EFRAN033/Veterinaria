# Guía de Instalación y Despliegue (SETUP_GUIDE)

Esta guía detalla cómo configurar el entorno de desarrollo local y cómo desplegar la aplicación en Render.com.

## 🛠️ Configuración Local (Para Desarrolladores)

### Prerrequisitos
- Python 3.10+
- Node.js 18+
- PostgreSQL

### 1. Base de Datos
Crea una base de datos PostgreSQL local:
```sql
CREATE DATABASE veterinaria_db;
```

### 2. Backend (FastAPI)

1.  Navega a la carpeta del backend:
    ```bash
    cd back_veterinaria
    ```
2.  Crea un entorno virtual y actívalo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate  # Windows
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configura las variables de entorno:
    Crea un archivo `.env` en `back_veterinaria/` con el siguiente contenido:
    ```ini
    PROJECT_NAME="Veterinaria API"
    API_V1_STR="/api/v1"
    SECRET_KEY="tu_clave_secreta_super_segura"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=11520
    
    # Base de datos (Ajusta usuario:password)
    DATABASE_URL="postgresql://postgres:tu_password@localhost/veterinaria_db"
    
    # OpenAI (Necesario para el Chat IA)
    OPENAI_API_KEY="sk-..."
    
    # Configuración CORS (Frontend URL)
    BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
    ```
5.  **Inicializar Base de Datos (Migraciones)**:
    Esto creará todas las tablas automáticamente.
    ```bash
    alembic upgrade head
    ```
    *Nota: Si es la primera vez, asegúrate de que la DB esté vacía o limpia.*

6.  **Crear Usuario Administrador (Root)**:
    Puedes crear un script o insertar manualmente en la DB, o usar el endpoint de registro si está habilitado.
    *Para producción, se recomienda tener un script de "seed" inicial.*

7.  Ejecutar el servidor:
    ```bash
    uvicorn main:app --reload
    ```

### 3. Frontend (Vue.js)

1.  Navega a la carpeta del frontend:
    ```bash
    cd front_veterinaria
    ```
2.  Instala dependencias:
    ```bash
    npm install
    ```
3.  Configura variables de entorno:
    Crea `.env.development`:
    ```ini
    VITE_API_URL=http://localhost:8000/api/v1
    VITE_BACKEND_URL=http://localhost:8000
    ```
4.  Ejecutar:
    ```bash
    npm run dev
    ```

---

## 🚀 Despliegue en Render.com

Render es una excelente opción para desplegar este proyecto. Necesitarás dos servicios: uno para el **Web Service** (Backend) y otro para el **Static Site** (Frontend), más una **PostgreSQL Database**.

### Paso 1: Base de Datos (PostgreSQL)
1.  En el Dashboard de Render, crea una **New PostgreSQL**.
2.  Nombre: `veterinaria-db`.
3.  Copia la **Internal Database URL** (para el backend en Render) y la **External Database URL** (si necesitas conectarte desde tu PC).

### Paso 2: Backend (Web Service)
1.  Crea un **New Web Service**.
2.  Conecta tu repositorio de GitHub.
3.  **Root Directory**: `back_veterinaria`
4.  **Build Command**: `pip install -r requirements.txt`
5.  **Start Command**: `alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 10000`
6.  **Environment Variables**:
    - `PYTHON_VERSION`: `3.10.0` (o superior)
    - `DATABASE_URL`: (Pega la Internal Database URL del Paso 1)
    - `SECRET_KEY`: (Genera una segura)
    - `OPENAI_API_KEY`: (Tu llave de OpenAI)
    - `BACKEND_CORS_ORIGINS`: `["https://tu-frontend-en-render.onrender.com"]` (Añade la URL de tu frontend cuando la tengas)
7.  **Despliegue**: Al desplegar, Render instalará dependencias, ejecutará las migraciones automáticamente y luego arrancará el servidor.
    *Nota: Al usar el comando de inicio combinado, no necesitas acceso a la Shell.*

### Paso 3: Frontend (Static Site)
1.  Crea un **New Static Site**.
2.  Conecta el mismo repositorio.
3.  **Root Directory**: `front_veterinaria`
4.  **Build Command**: `npm install && npm run build`
5.  **Publish Directory**: `dist`
6.  **Environment Variables**:
    - `VITE_API_URL`: `https://tu-backend-en-render.onrender.com/api/v1`
    - `VITE_BACKEND_URL`: `https://tu-backend-en-render.onrender.com`
7.  **Rewrite Rules** (Importante para Vue Router):
    - Ve a la pestaña **Redirects/Rewrites**.
    - Añade una regla:
        - **Source**: `/*`
        - **Destination**: `/index.html`
        - **Action**: `Rewrite`
8.  Guarda y despliega.

¡Listo! Tu sistema debería estar funcionando en la nube.

## ⚠️ Solución de Problemas Comunes

### Error CORS o "Network Error" al intentar Login/Registro
Si ves errores como `Solicitud de origen cruzado bloqueada` o intentos de conexión a `api.veterinaria.com`:

1.  **Revisa las Variables de Entorno del Frontend en Render**:
    *   Asegúrate de que `VITE_API_URL` apunte a tu **URL REAL del Backend en Render** (ej: `https://veterinaria-backend.onrender.com/api/v1`), NO a una URL de ejemplo.
    *   Asegúrate de que `VITE_BACKEND_URL` apunte a la raíz del backend (ej: `https://veterinaria-backend.onrender.com`).
    *   **Importante**: Después de cambiar variables en el Frontend, debes hacer un **Manual Deploy > Deploy latest commit** o **Clear build cache & deploy** para que los cambios surtan efecto, ya que Vite "quema" estas variables al momento de construir (build).

2.  **Revisa las Variables de Entorno del Backend en Render**:
    *   Asegúrate de que `BACKEND_CORS_ORIGINS` incluya la URL de tu frontend **sin barra al final** (ej: `["https://veterinaria-frontend.onrender.com"]`).
    *   Si cambias esto, el backend se reiniciará automáticamente.
