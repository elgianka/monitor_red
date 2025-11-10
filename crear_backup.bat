@echo off
echo Creando copia de seguridad del proyecto...
echo.

:: Genera un nombre de archivo con fecha y hora (YYYY-MM-DD_HH-MM)
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%h%TIME:~3,2%m

set BACKUP_FILENAME=monitoreo-com-backup-%TIMESTAMP%.zip

echo Comprimiendo archivos en: %BACKUP_FILENAME%
echo (Esto puede tardar unos momentos)...

:: Usa PowerShell para comprimir el directorio actual.
:: Se excluyen el directorio .git, el entorno virtual y el propio backup.
powershell.exe -NoProfile -Command "Get-ChildItem -Path '.' -Exclude '.git', '.venv', '*.zip' | Compress-Archive -DestinationPath '%BACKUP_FILENAME%' -Force"

echo.
echo ----------------------------------------------------
echo  Copia de seguridad creada exitosamente.
echo  Archivo: %BACKUP_FILENAME%
echo ----------------------------------------------------
echo.
pause
