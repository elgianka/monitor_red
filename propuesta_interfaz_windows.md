# Propuesta de Interfaz de Escritorio (Windows)

Esta aplicación será la **herramienta principal de gestión y operación** para los administradores de red, ofreciendo el conjunto más completo de funcionalidades y el mayor nivel de detalle.

*   **Rol Principal:** Gestión, configuración y monitoreo exhaustivo del sistema.
*   **Tecnología Propuesta:** **.NET con WinUI 3 y C#**.
    *   **Justificación:** Es la tecnología más moderna de Microsoft para crear interfaces de escritorio nativas. Asegura una integración perfecta con el look & feel de Windows 11, un rendimiento óptimo y acceso a todas las capacidades del sistema operativo.
*   **Arquitectura:** Patrón **MVVM (Model-View-ViewModel)**.
    *   **Justificación:** Es el estándar para aplicaciones XAML (WinUI/WPF). Separa limpiamente la interfaz (View) de la lógica de presentación (ViewModel) y los datos (Model), lo que resulta en un código más limpio, testeable y fácil de mantener.
*   **Vistas y Componentes Clave:**
    1.  **Dashboard Principal (Vista de Mando):**
        *   **Mapa Geográfico Interactivo:** Visualización de sedes y equipos (`TB_UBICACION`) con iconos que cambian de color según el estado de las alertas (`TB_ALERTA`).
        *   **Gráficos en Tiempo Real:** Paneles para latencia promedio, distribución de hosts por estado (`TB_ESTADO`), y un feed de las últimas alertas.
        *   **Resumen Global:** Tarjetas con contadores clave (Hosts totales, activos, caídos, alertas activas).
    2.  **Gestión de Inventario (ABM de `TB_HOST`):**
        *   Una **tabla de datos avanzada** con capacidades de filtrado, búsqueda y ordenamiento en todas las columnas.
        *   Formularios para la **creación y edición de hosts**, utilizando los catálogos (`TB_MODELO`, `TB_RESPONSABLE`) para rellenar listas desplegables y asegurar la integridad de los datos.
    3.  **Análisis de Host Individual:**
        *   Vista detallada con toda la información de un host y un **gráfico histórico de su latencia** (`TB_MONITOREO`) con capacidad de zoom y selección de rangos de fechas.
    4.  **Administración de Catálogos:**
        *   Sección dedicada a la gestión de todos los datos maestros (`TB_GERENCIA`, `TB_AREA`, `TB_MARCA`, etc.).
*   **Consideraciones de Diseño y UX:**
    *   **Notificaciones Nativas de Windows:** Integración con el centro de notificaciones para mostrar alertas críticas de forma no intrusiva.
    *   **Menús Contextuales:** Clic derecho sobre los hosts para acciones rápidas ("Ver detalles", "Reconocer alerta").
    *   **Temas:** Soportar modos claro y oscuro para adaptarse a las preferencias del usuario y del sistema operativo.
