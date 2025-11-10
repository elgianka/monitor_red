@echo off
cd d:\Dropbox\DEV\MONITOREO-COM
echo Activando entorno virtual...
call .\.venv\Scripts\activate.bat
echo.
echo Intentando iniciar la API...
uvicorn api.main:app --host 127.0.0.1 --port 8000
pause
