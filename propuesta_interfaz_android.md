# Propuesta de Interfaz Móvil (Android)

Diseñada para la **movilidad y la respuesta rápida**, esta aplicación permite al personal de TI supervisar la red y reaccionar a incidentes desde cualquier lugar.

*   **Rol Principal:** Monitoreo en tiempo real y gestión de alertas sobre la marcha.
*   **Tecnología Propuesta:** **Kotlin con Jetpack Compose**.
    *   **Justificación:** Es el framework de UI moderno, declarativo y recomendado por Google para Android. Permite crear interfaces fluidas y reactivas con una base de código más concisa y mantenible.
*   **Arquitectura:** **MVVM + Clean Architecture**.
    *   **Justificación:** Separar la lógica en capas bien definidas (UI, ViewModel, Casos de Uso, Repositorios) es crucial para construir una aplicación móvil que sea robusta, escalable, fácil de testear y con un buen rendimiento.
*   **Vistas y Componentes Clave:**
    1.  **Dashboard Simplificado:**
        *   Una lista que prioriza los **hosts con problemas** (estado "Caído" o con alertas activas).
        *   Un resumen numérico y claro del estado general de la red.
    2.  **Feed de Alertas:**
        *   La vista principal será una lista de `TB_ALERTA` activas, presentada como un feed de notificaciones.
        *   Permitirá al usuario **"silenciar" o "reconocer" una alerta** con un simple gesto de swipe, ejecutando la acción correspondiente en el backend a través de la API.
    3.  **Detalles del Host:**
        *   Una vista simple con la información más crítica del host y un gráfico de su latencia en las últimas 24 horas.
*   **Consideraciones de Diseño y UX:**
    *   **Notificaciones Push Críticas:** Integración obligatoria con **Firebase Cloud Messaging (FCM)**. Cuando la API genere una alerta crítica, debe poder enviar una notificación push para alertar al usuario de inmediato, incluso si la app está cerrada.
    *   **Diseño "Mobile-First":** La interfaz debe ser extremadamente simple, con alta legibilidad y botones grandes para facilitar el uso con una sola mano en condiciones no ideales.
    *   **Optimización:** Minimizar el uso de datos y batería mediante estrategias de caché y llamadas eficientes a la API.
