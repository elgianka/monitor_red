@echo off
echo Activando entorno virtual y ejecutando script de creacion manual...
call .\.venv\Scripts\activate.bat
python .\api\manual_create_admin.py
pause
