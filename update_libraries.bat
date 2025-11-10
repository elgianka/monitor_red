@echo off
echo Activando entorno virtual y actualizando bibliotecas...
call .\.venv\Scripts\activate.bat
pip install --upgrade passlib bcrypt
echo.
echo Actualizacion completada.
pause
