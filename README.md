# Sistema de Gestión Veterinaria con IA y DSS

Este es un sistema integral para la gestión de clínicas veterinarias, potenciado con Inteligencia Artificial y un Sistema de Soporte a la Decisión (DSS).

## Características Principales

### 🏥 Gestión Clínica
- **Agenda y Citas**: Calendario interactivo para veterinarios.
- **Historial Médico**: Registro completo de pacientes.
- **Solicitudes de Servicio**: Gestión de peticiones de clientes.

### 🧠 Inteligencia Artificial y DSS
- **Chatbot Veterinario**: Asistente IA (OpenAI) con contexto clínico.
- **Triaje Automático**: Algoritmos deterministas para evaluar constantes vitales (Índice de Shock, Deshidratación).
- **Predicción de Gravedad**: Modelo de Machine Learning local (Random Forest) para estimar el riesgo del paciente.
- **Dashboard DSS**: Visualización en tiempo real de alertas y predicciones.

### 💻 Plataforma Web
- **Frontend Moderno**: Vue 3 + Vite + TailwindCSS.
- **Adopción Online**: Módulo para publicar y gestionar adopciones.
- **Pet Shop**: Catálogo de productos.

## Tecnologías

- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy, Alembic.
- **Frontend**: Vue.js 3, Pinia, Vue Router, TailwindCSS.
- **IA/ML**: OpenAI API, Scikit-learn, Pandas.
- **Infraestructura**: Docker ready, Render compatible.

## Empezar

Para instrucciones detalladas de instalación y despliegue, consulta el archivo [SETUP_GUIDE.md](./SETUP_GUIDE.md).
