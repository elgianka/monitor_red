@echo off
echo Activando entorno virtual e instalando dependencias...
call .\.venv\Scripts\activate.bat
pip install -r .\api\requirements.txt
pip install -r .\windows_app\requirements.txt
echo.

echo Instalacion completada.
pause
