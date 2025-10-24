# Reporte del Esquema de la Base de Datos

Este documento detalla la estructura final de la base de datos `monitor_ping.db`.

## Tablas de Catálogo (Datos Maestros)

Estas tablas contienen la información descriptiva y organizacional que rara vez cambia.

### `GERENCIA`
Almacena las gerencias de la organización.
- `ID_GERENCIA`: Llave Primaria (Entero)
- `NOM_GERENCIA`: Nombre de la gerencia (Texto, Requerido)

### `AREA`
Almacena las áreas, vinculadas a una gerencia.
- `ID_AREA`: Llave Primaria (Entero)
- `NOM_AREA`: Nombre del área (Texto, Requerido)
- `ID_GERENCIA`: Vínculo a `GERENCIA`

### `PROCESO`
Almacena los procesos de negocio a los que puede estar asociado un equipo.
- `ID_PROCESO`: Llave Primaria (Entero)
- `NOM_PROCESO`: Nombre del proceso (Texto, Requerido)
- `DET_PROCESO`: Descripción del proceso (Texto)

### `SEDE`
Almacena las sedes o locales físicos de la empresa.
- `ID_SEDE`: Llave Primaria (Entero)
- `NOM_SEDE`: Nombre de la sede (Texto, Requerido)

### `UBICACION`
Define una ubicación específica dentro de una sede, con coordenadas para el mapa.
- `ID_UBICACION`: Llave Primaria (Entero)
- `NOM_UBICACION`: Nombre de la ubicación (Texto, Requerido)
- `COORD_UBICACION`: Coordenadas geográficas (Texto)
- `ID_SEDE`: Vínculo a `SEDE`

### `CATEGORIA`
Clasificación de los equipos (e.g., Switch, Router, Access Point).
- `ID_CATEGORIA`: Llave Primaria (Entero)
- `NOM_CATEGORIA`: Nombre de la categoría (Texto, Requerido)

### `MARCA`
Marcas de los equipos de comunicación (e.g., Cisco, Ubiquiti, Mikrotik).
- `ID_MARCA`: Llave Primaria (Entero)
- `NOM_MARCA`: Nombre de la marca (Texto, Requerido)

### `MODELO`
Modelos específicos de equipos, vinculados a una marca.
- `ID_MODELO`: Llave Primaria (Entero)
- `NOM_MODELO`: Nombre del modelo (Texto, Requerido)
- `ID_MARCA`: Vínculo a `MARCA`

### `RESPONSABLE`
Personas responsables de los equipos, vinculadas a un área.
- `ID_RESPONSABLE`: Llave Primaria (Entero)
- `NOM_RESPONSABLE`: Nombre del responsable (Texto, Requerido)
- `ID_AREA`: Vínculo a `AREA`

### `ESTADO`
Define el ciclo de vida de un equipo (e.g., Activo, Mantenimiento, Baja).
- `ID_ESTADO`: Llave Primaria (Entero)
- `NOM_ESTADO`: Nombre del estado (Texto, Requerido, Único)

### `USUARIOS_DEL_SISTEMA`
Gestiona el acceso a la aplicación de monitoreo.
- `ID_USUARIO`: Llave Primaria (Entero)
- `NOM_USUARIO`: Nombre de usuario para login (Texto, Requerido, Único)
- `PASSWORD_HASH`: Contraseña cifrada (Texto, Requerido)
- `ROL`: Rol del usuario para permisos (Texto, Requerido)

---

## Tablas Transaccionales (Datos Variables)

Estas tablas almacenan los datos que cambian constantemente como resultado de las operaciones del sistema.

### `HOST`
El corazón del sistema. Define cada equipo a monitorear y lo relaciona con toda su información descriptiva.
- `ID_HOST`: Llave Primaria (Entero)
- `NOM_HOST`: Nombre descriptivo del equipo (Texto, Requerido)
- `IP_HOST`: Dirección IP a monitorear (Texto, Requerido, Único)
- `MAC_HOST`: Dirección MAC del equipo (Texto)
- `NUM_SERIE`: Número de serie del equipo (Texto)
- `FECHA_ALTA`: Fecha de registro del equipo (Fecha)
- `AÑO_ALTA`: Año de registro del equipo (Entero)
- `ID_MODELO`: Vínculo a `MODELO`
- `ID_RESPONSABLE`: Vínculo a `RESPONSABLE`
- `ID_UBICACION`: Vínculo a `UBICACION`
- `ID_PROCESO`: Vínculo a `PROCESO`
- `ID_CATEGORIA`: Vínculo a `CATEGORIA`
- `ID_ESTADO`: Vínculo a `ESTADO`
- `LIM_SUP_PING`: Límite superior de latencia para alertas (Numérico)
- `LIM_INF_PING`: Límite inferior de latencia para alertas (Numérico)

### `MONITOREO`
Es el log histórico. Registra cada intento de ping a un host.
- `ID_MONITOREO`: Llave Primaria (Entero)
- `ID_HOST`: Vínculo al `HOST` monitoreado
- `PING_RESULT`: El resultado del ping (e.g., latencia en ms, 0 si no responde)
- `TIMESTAMP`: Fecha y hora exactas del monitoreo (Fecha/Hora)
