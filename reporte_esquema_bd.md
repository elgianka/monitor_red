# Reporte del Esquema de la Base de Datos

Este documento detalla la estructura final de la base de datos `monitor_ping.db`.

## Tablas de Catálogo (Datos Maestros)

Estas tablas contienen la información descriptiva y organizacional que rara vez cambia.

### `TB_GERENCIA`
Almacena las gerencias de la organización.
- `ID_GERENCIA`: Llave Primaria (Entero)
- `NOM_GERENCIA`: Nombre de la gerencia (Texto, Requerido)

### `TB_AREA`
Almacena las áreas, vinculadas a una gerencia.
- `ID_AREA`: Llave Primaria (Entero)
- `NOM_AREA`: Nombre del área (Texto, Requerido)
- `ID_GERENCIA`: Vínculo a `TB_GERENCIA`

### `TB_PROCESO`
Almacena los procesos de negocio a los que puede estar asociado un equipo.
- `ID_PROCESO`: Llave Primaria (Entero)
- `NOM_PROCESO`: Nombre del proceso (Texto, Requerido)
- `DET_PROCESO`: Descripción del proceso (Texto)

### `TB_SEDE`
Almacena las sedes o locales físicos de la empresa.
- `ID_SEDE`: Llave Primaria (Entero)
- `NOM_SEDE`: Nombre de la sede (Texto, Requerido)

### `TB_UBICACION`
Define una ubicación específica dentro de una sede, con coordenadas para el mapa.
- `ID_UBICACION`: Llave Primaria (Entero)
- `NOM_UBICACION`: Nombre de la ubicación (Texto, Requerido)
- `COORD_UBICACION`: Coordenadas geográficas (Texto)
- `ID_SEDE`: Vínculo a `TB_SEDE`

### `TB_CATEGORIA`
Clasificación de los equipos (e.g., Switch, Router, Access Point).
- `ID_CATEGORIA`: Llave Primaria (Entero)
- `NOM_CATEGORIA`: Nombre de la categoría (Texto, Requerido)

### `TB_MARCA`
Marcas de los equipos de comunicación (e.g., Cisco, Ubiquiti, Mikrotik).
- `ID_MARCA`: Llave Primaria (Entero)
- `NOM_MARCA`: Nombre de la marca (Texto, Requerido)

### `TB_MODELO`
Modelos específicos de equipos, vinculados a una marca.
- `ID_MODELO`: Llave Primaria (Entero)
- `NOM_MODELO`: Nombre del modelo (Texto, Requerido)
- `ID_MARCA`: Vínculo a `TB_MARCA`

### `TB_RESPONSABLE`
Personas responsables de los equipos, vinculadas a un área.
- `ID_RESPONSABLE`: Llave Primaria (Entero)
- `NOM_RESPONSABLE`: Nombre del responsable (Texto, Requerido)
- `ID_AREA`: Vínculo a `TB_AREA`

### `TB_ESTADO`
Define el ciclo de vida de un equipo (e.g., Activo, Mantenimiento, Baja).
- `ID_ESTADO`: Llave Primaria (Entero)
- `NOM_ESTADO`: Nombre del estado (Texto, Requerido, Único)

### `TB_USUARIOS_DEL_SISTEMA`
Gestiona el acceso a la aplicación de monitoreo.
- `ID_USUARIO`: Llave Primaria (Entero)
- `NOM_USUARIO`: Nombre de usuario para login (Texto, Requerido, Único)
- `PASSWORD_HASH`: Contraseña cifrada (Texto, Requerido)
- `ROL`: Rol del usuario para permisos (Texto, Requerido)

---

## Tablas Transaccionales (Datos Variables)

Estas tablas almacenan los datos que cambian constantemente como resultado de las operaciones del sistema.

### `TB_HOST`
El corazón del sistema. Define cada equipo a monitorear y lo relaciona con toda su información descriptiva.
- `ID_HOST`: Llave Primaria (Entero)
- `NOM_HOST`: Nombre descriptivo del equipo (Texto, Requerido)
- `IP_HOST`: Dirección IP a monitorear (Texto, Requerido, Único)
- `MAC_HOST`: Dirección MAC del equipo (Texto)
- `NUM_SERIE`: Número de serie del equipo (Texto)
- `FIRMWARE_VERSION`: Versión del firmware del equipo (Texto)
- `FECHA_ALTA`: Fecha de registro del equipo (Fecha)
- `AÑO_ALTA`: Año de registro del equipo (Entero)
- `ID_MODELO`: Vínculo a `TB_MODELO`
- `ID_RESPONSABLE`: Vínculo a `TB_RESPONSABLE`
- `ID_UBICACION`: Vínculo a `TB_UBICACION`
- `ID_PROCESO`: Vínculo a `TB_PROCESO`
- `ID_CATEGORIA`: Vínculo a `TB_CATEGORIA`
- `ID_ESTADO`: Vínculo a `TB_ESTADO`
- `LIM_SUP_PING`: Límite superior de latencia para alertas (Numérico)
- `LIM_INF_PING`: Límite inferior de latencia para alertas (Numérico)

### `TB_MONITOREO`
Es el log histórico. Registra cada intento de ping a un host.
- `ID_MONITOREO`: Llave Primaria (Entero)
- `ID_HOST`: Vínculo al `TB_HOST` monitoreado
- `PING_RESULT`: El resultado del ping (e.g., latencia en ms, 0 si no responde)
- `TIMESTAMP`: Fecha y hora exactas del monitoreo (Fecha/Hora)

---

## Nuevas Tablas (v2)

### `TB_ALERTA`
Registra y gestiona eventos que requieren atención, como un host caído o con latencia anómala.
- `ID_ALERTA`: Llave Primaria (Entero)
- `ID_HOST`: Vínculo al `TB_HOST`
- `TIPO_ALERTA`: Describe el tipo de alerta (e.g., 'CAIDO', 'LATENCIA_ALTA')
- `ESTADO_ALERTA`: Estado actual de la alerta (e.g., 'ACTIVA', 'RESUELTA')
- `TIMESTAMP_INICIO`: Fecha y hora de inicio de la alerta
- `TIMESTAMP_FIN`: Fecha y hora de resolución de la alerta
- `ID_MONITOREO_INICIO`: Vínculo al log que disparó la alerta

### `TB_EVENTO_SISTEMA`
Guarda un registro de auditoría de todas las acciones importantes realizadas en el sistema.
- `ID_EVENTO`: Llave Primaria (Entero)
- `ID_USUARIO`: Vínculo a `TB_USUARIOS_DEL_SISTEMA` (quién realizó la acción)
- `TIPO_EVENTO`: Tipo de acción realizada (e.g., 'HOST_CREADO', 'LOGIN_FALLIDO')
- `DETALLES_EVENTO`: Descripción en texto o JSON de la acción
- `IP_ORIGEN`: Dirección IP desde donde se realizó la acción
- `TIMESTAMP`: Fecha y hora del evento

### `TB_CONFIGURACION_SISTEMA`
Almacena parámetros de configuración de la aplicación para permitir cambios sin redesplegar código.
- `CLAVE`: Llave primaria. Nombre del parámetro (e.g., 'UMBRAL_LATENCIA_DEFAULT')
- `VALOR`: Valor del parámetro
- `DESCRIPCION`: Explicación del propósito del parámetro
- `ULTIMA_MODIFICACION`: Fecha de la última actualización

### `TB_NOTIFICACION`
Lleva un registro de todas las notificaciones enviadas a los usuarios.
- `ID_NOTIFICACION`: Llave Primaria (Entero)
- `ID_ALERTA`: Vínculo a la `TB_ALERTA` que generó la notificación
- `CANAL`: Medio por el cual se envió (e.g., 'EMAIL', 'SMS', 'SLACK')
- `DESTINATARIO`: Dirección o contacto del receptor
- `CONTENIDO`: Cuerpo del mensaje enviado
- `ESTADO`: Estado del envío (e.g., 'ENVIADA', 'FALLIDA')
- `TIMESTAMP`: Fecha y hora del envío