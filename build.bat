@echo off
chcp 65001 > nul

echo ========================================
echo    NBiblioteca — Setup
echo ========================================

echo.
echo [1/5] Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 ( echo ERROR en instalacion de dependencias & exit /b 1 )

echo.
echo [2/5] Aplicando migraciones...
python manage.py migrate --run-syncdb
if errorlevel 1 ( echo ERROR en migraciones & exit /b 1 )

echo.
echo [3/5] Creando superusuario (admin / admin)...
python manage.py createsu
if errorlevel 1 ( echo ERROR al crear superusuario & exit /b 1 )

echo.
echo [4/5] Creando roles y permisos...
python manage.py crear_roles
if errorlevel 1 ( echo ERROR al crear roles & exit /b 1 )

echo.
echo [5/5] Poblando datos de ejemplo...
python manage.py poblar_datos
if errorlevel 1 ( echo ERROR al poblar datos & exit /b 1 )

echo.
echo ========================================
echo   Listo. Ejecuta el servidor con:
echo   python manage.py runserver
echo ========================================
