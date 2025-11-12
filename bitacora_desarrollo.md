## 2025-11-11 - Solución al problema de carga de Sedes en la aplicación de Windows

### Descripción
Se identificó que el campo "Sedes" no cargaba en la aplicación de Windows al intentar añadir un nuevo host, debido a que la tabla `sedes` en la base de datos estaba vacía. La API de `sedes` no requiere autenticación, por lo que el problema no residía en la comunicación o autenticación, sino en la ausencia de datos iniciales.

### Cambios Realizados:

1.  **`create_database_and_admin.py`**:
    *   Se modificó el script para incluir la inserción de sedes por defecto ("Oficina Principal", "Sucursal Norte", "Sucursal Sur") si la tabla `sedes` se encuentra vacía al ejecutar el script.

### Pasos para verificar la solución:

1.  **Ejecutar el script `create_database_and_admin.py`**: Esto poblará la tabla `sedes` con los datos por defecto.
2.  **Reiniciar la API**: Asegurarse de que la API esté ejecutándose para que la aplicación de Windows pueda acceder a los nuevos datos.
3.  **Reiniciar la aplicación de Windows**: Abrir la aplicación y verificar que el campo "Sedes" en el diálogo de añadir host ahora muestra las opciones por defecto.

### Conclusión:
Con estos cambios, la aplicación de Windows debería poder cargar y mostrar las sedes correctamente, permitiendo la adición de nuevos hosts.

---

## 2025-11-11 - Reaparición del error de autenticación (401 Unauthorized)

### Descripción
El usuario reporta que el error de autenticación "401 Client Error: Unauthorized for url: http://127.0.0.1:8000/api/v1/token" ha reaparecido. Este error indica que las credenciales utilizadas para autenticarse contra la API son incorrectas o inválidas.

### Cambios Realizados:

1.  **`create_database_and_admin.py`**:
    *   Se añadió una declaración `print` para confirmar explícitamente que la contraseña del usuario 'admin' ha sido actualizada o establecida durante la ejecución del script. Esto ayuda a verificar que el script está funcionando como se espera en relación con las credenciales del usuario administrador.

### Pasos para verificar la solución:

1.  **Ejecutar el script `create_database_and_admin.py`**: Es crucial ejecutar este script para asegurar que el usuario 'admin' exista y tenga la contraseña correcta en la base de datos. La salida de la consola debería mostrar "Admin user setup complete."
2.  **Reiniciar la API**: Asegurarse de que la API esté ejecutándose.
3.  **Reiniciar la aplicación de Windows**: Abrir la aplicación e intentar iniciar sesión con las credenciales 'admin'/'admin'.

### Conclusión:
Al asegurar que el script `create_database_and_admin.py` se ejecute correctamente y que la aplicación de Windows utilice las credenciales 'admin'/'admin', el problema de autenticación debería resolverse.

---

## 2025-11-11 - Solución al error de inicialización de la base de datos (sqlite3.OperationalError)

### Descripción
El usuario reporta el error `(sqlite3.OperationalError) table TB_UBICACION has no column named ID_SEDE` durante la inicialización de la base de datos. Esto indica una inconsistencia entre el esquema de la base de datos existente y los modelos definidos en la API, específicamente que la tabla `TB_UBICACION` no tiene la columna `ID_SEDE` esperada.

### Causa Identificada:
La base de datos `monitor_ping.db` no estaba sincronizada con los modelos de SQLAlchemy, probablemente debido a cambios en los modelos que no se reflejaron en el archivo de la base de datos.

### Cambios Realizados:
No se realizaron cambios en el código. La solución implica una acción manual por parte del usuario.

### Pasos para verificar la solución:

1.  **Eliminar el archivo de la base de datos `monitor_ping.db`**: Este archivo se encuentra en `d:\Dropbox\DEV\MONITOREO-COM\api\monitor_ping.db`. **Es crucial eliminar este archivo para forzar la recreación de la base de datos con el esquema actualizado.**
2.  **Ejecutar el script `create_database_and_admin.py`**: Esto recreará la base de datos `monitor_ping.db` con el esquema correcto, incluyendo todas las tablas y columnas necesarias, y poblará el usuario 'admin' y las sedes por defecto.
3.  **Reiniciar la API**: Asegurarse de que la API esté ejecutándose.
4.  **Reiniciar la aplicación de Windows**: Abrir la aplicación e intentar iniciar sesión.

### Conclusión:
Al eliminar el archivo de la base de datos desactualizado y permitir que el script de creación de la base de datos la regenere, se resolverá la inconsistencia del esquema y se eliminará el `sqlite3.OperationalError`.

### Próximos Pasos:
*   Esperar la confirmación del usuario sobre la solución y continuar con las siguientes tareas.