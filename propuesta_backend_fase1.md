# Propuesta Backend Fase 1: Conexión a BD y Primer Endpoint

1.  **Crear la Lógica de Conexión:**
    *   Se creará el archivo `api/db/session.py` que se encargará de gestionar la conexión con la base de datos `monitor_ping.db` usando SQLAlchemy.
2.  **Definir el Modelo de Datos:**
    *   Se creará el archivo `api/models/host.py` que contendrá el modelo Pydantic para la tabla `TB_HOST`. Esto permitirá validar y estructurar los datos que se envían y reciben.
3.  **Implementar el Primer Endpoint Real:**
    *   Se creará el archivo `api/routers/hosts.py` y dentro de él, se implementará el endpoint `GET /api/v1/hosts` que leerá los equipos desde la base de datos y los devolverá como una respuesta JSON.
