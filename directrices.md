# Directrices del Proyecto: Monitoreo de Comunicaciones

Este documento sirve como una guía de referencia para el desarrollo del proyecto de monitoreo de comunicaciones.

## 1. Plataformas

*   **Aplicación de Escritorio:** La aplicación principal de monitoreo debe funcionar en Windows.
*   **Aplicación Móvil:** Se requiere una aplicación complementaria para Android.
*   **Reportes:** Los reportes y visualizaciones se deben presentar en una interfaz web.

## 2. Principios de Diseño

*   **Modularidad:** El sistema debe estar diseñado en módulos independientes para facilitar el mantenimiento y la escalabilidad.
*   **Modernidad:** Utilizar tecnologías y arquitecturas modernas.
*   **Escalabilidad:** La arquitectura debe permitir el crecimiento futuro en términos de carga y funcionalidades.

## 3. Funcionalidades Clave

*   **Monitoreo de Red:** Realizar pings constantes desde la aplicación de escritorio a una lista configurable de hosts (equipos de comunicaciones).
*   **Mapa de Equipos:** Mostrar un mapa con la ubicación geográfica de los equipos monitoreados.

## 4. Base de Datos

*   **Producción:** El objetivo a largo plazo es utilizar SQL Server.
*   **Desarrollo Inicial:** Para la fase actual, se utilizará SQLite.

## 5. Evolución del Proyecto

Este documento es una guía viva. Se irá actualizando y enriqueciendo a medida que surjan nuevas funcionalidades, requisitos o necesidades durante el desarrollo del proyecto.
