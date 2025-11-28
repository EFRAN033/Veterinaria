# Sistema de Gestión Veterinaria con IA

Este es un sistema integral para clínicas veterinarias que incluye gestión de citas, historial médico, adopciones y un asistente de Inteligencia Artificial para apoyo clínico.

## 🚀 Características

- **Gestión de Citas**: Calendario interactivo para veterinarios y clientes.
- **Historia Clínica**: Registro digital de mascotas y tratamientos.
- **Asistente IA**: Chatbot especializado en medicina veterinaria para apoyo en triaje y diagnóstico.
- **Adopciones**: Módulo público para adopción de mascotas.
- **Roles**: Accesos diferenciados para Veterinarios, Administradores y Clientes.

## 🛠️ Tecnologías

- **Backend**: Python (FastAPI), SQLAlchemy, PostgreSQL, Alembic.
- **Frontend**: Vue.js 3, Vite, TailwindCSS, Pinia.
- **IA**: OpenAI API.
- **Base de Datos**: PostgreSQL.

## 📋 Requisitos Previos

Asegúrate de tener instalado:

- [Python 3.9+](https://www.python.org/)
- [Node.js 16+](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 💻 Instalación y Ejecución Local

### 1. Configuración del Backend

1.  Navega a la carpeta del backend:

    ```bash
    cd back_veterinaria
    ```

2.  Crea un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configura las variables de entorno:

    - Crea un archivo `.env` (basado en el que ya tienes configurado).
    - Asegúrate de tener la `DATABASE_URL` apuntando a tu PostgreSQL local.

5.  Inicia el servidor:
    ```bash
    uvicorn main:app --reload
    ```
    El backend correrá en `http://localhost:8000`.

### 2. Configuración del Frontend

1.  Navega a la carpeta del frontend:

    ```bash
    cd front_veterinaria
    ```

2.  Instala las dependencias:

    ```bash
    npm install
    ```

3.  Inicia el servidor de desarrollo:
    ```bash
    npm run dev
    ```
    El frontend correrá en `http://localhost:5173`.

---

## 🗄️ Base de Datos

### Importar Base de Datos Local

Si tienes un archivo `.sql` de respaldo:

```bash
psql -U tu_usuario -d nombre_db < respaldo.sql
```

### Migraciones con Alembic

Si estás desarrollando y cambiaste los modelos:

1.  Genera una nueva migración:
    ```bash
    alembic revision --autogenerate -m "descripcion_cambio"
    ```
2.  Aplica los cambios:
    ```bash
    alembic upgrade head
    ```

---

## ☁️ Despliegue y Migración a Render

### Migrar Base de Datos a Render

Tienes dos opciones principales:

#### Opción A: Copia Completa (Recomendada para mover datos)

Si quieres que tu base de datos en Render sea **idéntica** a la local (incluyendo usuarios, citas, etc.):

1.  Exporta tu DB local:
    ```bash
    pg_dump -U tu_usuario_local nombre_db_local > backup.sql
    ```
2.  Importa en Render (usando la "External Database URL" que te da Render):
    ```bash
    psql "postgres://usuario:password@host_render/db_name" < backup.sql
    ```

#### Opción B: Solo Estructura (Alembic)

Si solo quieres actualizar las tablas pero no los datos:

1.  En el script de "Build Command" o "Start Command" de Render, asegúrate de ejecutar:
    ```bash
    alembic upgrade head
    ```
    Esto aplicará las migraciones pendientes.

### ¿Está Alembic actualizado?

Para saber si tus migraciones están al día con tus modelos actuales, ejecuta en local:

```bash
alembic revision --autogenerate -m "check_updates"
```

- Si dice "no changes detected", estás al día.
- Si genera un archivo nuevo, significa que tenías cambios pendientes. Sube ese archivo a Git para que Render lo aplique.
