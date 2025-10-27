# Plan de Acción para el Desarrollo

## Premisa
El punto de partida indiscutible es el **backend (API REST)**. Sin una API funcional, ninguna de las interfaces de usuario (Windows, Android, Web) puede operar. Empezar por la API nos permite definir el "contrato" de datos que los clientes consumirán, permitiendo que el trabajo de los frontends pueda empezar en paralelo una vez definidos los primeros endpoints.

## Fases del Proyecto

### 1. Fase 1: Construir el Esqueleto de la API (Backend)
*   **Acción Inmediata:** Iniciar el proyecto de la API con **Python y FastAPI**. - **DONE**
*   **Primer Objetivo:** Implementar los **endpoints de solo lectura (GET)** para los datos más críticos. Esto desbloquea al resto del equipo para que puedan empezar a visualizar datos reales lo antes posible.
    *   `GET /api/v1/hosts` (para listar todos los equipos) - **DONE**
    *   `GET /api/v1/hosts/{id_host}` (para ver el detalle de un equipo) - **DONE**
    *   `GET /api/v1/alerts/active` (para listar las alertas activas) - **DONE**
*   **Segundo Objetivo:** Implementar la **autenticación**. Definir cómo los usuarios (`TB_USUARIOS_DEL_SISTEMA`) obtendrán un token (JWT) para poder realizar peticiones seguras. Esto es fundamental y debe hacerse al principio. - **DONE**

### 2. Fase 2: Iniciar Desarrollo en Paralelo (Frontends)
*   Una vez que los endpoints de la Fase 1 estén definidos, los equipos de frontend pueden empezar.
*   **Equipo de Windows:** Puede empezar a construir la **vista del Dashboard Principal** y la tabla de gestión de inventario.
*   **Equipo de Android:** Puede enfocarse en el **"Feed de Alertas"**.
*   **Equipo Web:** Puede comenzar a diseñar los **filtros y los componentes de gráficos**.

### 3. Fase 3: Completar la Lógica de la API (Backend)
*   Mientras los frontends avanzan, el equipo de backend continúa implementando los endpoints de **escritura (POST, PUT, DELETE)** para la gestión completa del sistema. - **DONE**

## Resumen del Kickoff
Nuestra primera tarea es **crear un nuevo directorio para la API (ej. `api/`) y empezar a escribir el código para el primer endpoint con FastAPI**.
