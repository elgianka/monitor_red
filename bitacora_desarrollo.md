## 2025-11-05 - Aplicación de Patrón de Colores a Etiquetas de Resumen

### Descripción
Se ha aplicado el patrón de colores (verde para activo, rojo para inactivo) a las etiquetas de resumen "TOTAL de Hosts Activos" y "TOTAL de Hosts Inactivos" en el Dashboard de la aplicación de Windows.

### Cambios Realizados:

1.  **`windows_app/views/dashboard_view.py`**:
    *   Se modificó la función `update_summary_values` para configurar el `text_color` de `self.active_hosts_frame.value_label` a verde (`#00FF00`) y `self.inactive_hosts_frame.value_label` a rojo (`#FF4D4D`).

### Próximos Pasos:
*   Verificación de la funcionalidad en la aplicación de Windows.
*   Ajustes de la interfaz de usuario si el problema de "fuera de línea" persiste.
*   Implementación de la lógica de alertas en la UI basada en los resultados de ping.

## 2025-11-05 - Corrección de Esquema de Base de Datos para Ubicación

### Descripción
Se corrigió la inconsistencia entre el modelo de SQLAlchemy `UbicacionDB` y el esquema de la base de datos `esquema_v2.sql` para la tabla `TB_UBICACION`. El esquema de la base de datos no incluía las columnas `LATITUD` y `LONGITUD`, lo que causaba un error `OperationalError` al intentar acceder a estas propiedades desde el modelo.

### Cambios Realizados:

1.  **`esquema_v2.sql`**:
    *   Se modificó la definición de la tabla `TB_UBICACION` para reemplazar la columna `COORD_UBICACION TEXT` por `LATITUD REAL` y `LONGITUD REAL`.

### Próximos Pasos:
*   Para que este cambio tenga efecto, se recomienda recrear la base de datos utilizando el `esquema_v2.sql` actualizado. Si existen datos, se deberá realizar una migración manual o utilizar una herramienta de migración de base de datos.