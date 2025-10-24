# Directrices de la Base de Datos

## 1. Motor de Base de Datos

*   **Motor actual:** SQLite.
*   **Consideraciones para migración:** El diseño debe ser lo más uniforme posible para facilitar una futura migración a SQL Server. Esto implica separar la lógica de negocio de la base de datos tanto como sea posible, para que en el futuro se pueda migrar a procedimientos almacenados (stored procedures) si es necesario.

## 2. Tablas

Se deben crear las siguientes tablas:

*   `HOST`
*   `CATEGORIA`
*   `MARCA`
*   `MODELO`
*   `SEDE`
*   `UBICACION`
*   `USUARIOS_DEL_SISTEMA`
*   `GERENCIA`
*   `AREA`
*   `PROCESO`
*   `RESPONSABLE`
*   `MONITOREO`

## 3. Estructura de las Tablas

### HOST
*   `ID_HOST`
*   `NOM_HOST`
*   `IP_HOST`
*   `MAC_HOST`
*   `MARCA`
*   `MODELO`
*   `RESPONSABLE`
*   `SEDE`
*   `UBICACION`
*   `GERENCIA`
*   `AREA`
*   `PROCESO`
*   `ID_RESPONSABLE`
*   `LIM_SUP_PING`
*   `LIM_INF_PING`

### CATEGORIA
*   `ID_CATEGORIA`
*   `NOM_CATEGORIA`

### MARCA
*   `ID_MARCA`
*   `NOM_MARCA`

### MODELO
*   `ID_MODELO`
*   `NOM_MODELO`

### RESPONSABLE
*   `ID_RESPONSABLE`
*   `NOM_RESPONSABLE`
*   `ID_GERENCIA`
*   `ID_AREA`

### SEDE
*   `ID_SEDE`
*   `NOM_SEDE`

### UBICACION
*   `ID_UBICACION`
*   `NOM_UBICACION`
*   `COORD_UBICACION`
*   `ID_SEDE`

### GERENCIA
*   `ID_GERENCIA`
*   `NOM_GERENCIA`

### AREA
*   `ID_AREA`
*   `NOM_AREA`
*   `ID_GERENCIA`

### PROCESO
*   `ID_PROCESO`
*   `NOM_PROCESO`
*   `DET_PROCESO`

### MONITOREO
*   `ID_HOST`
*   `PING`