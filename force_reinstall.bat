@echo off
echo Activando entorno virtual y forzando la reinstalacion COMPLETA de bibliotecas...
call .\.venv\Scripts\activate.bat
pip uninstall -y passlib bcrypt
pip install --force-reinstall --no-cache-dir "passlib[bcrypt]"
echo.
echo Reinstalacion completada.
pause
