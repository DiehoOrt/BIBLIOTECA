#!/usr/bin/env bash
set -e

echo "========================================"
echo "   NBiblioteca — Setup"
echo "========================================"

# 1. Dependencias
echo ""
echo "[1/4] Instalando dependencias..."
pip install -r requirements.txt --quiet

# 2. Migraciones
echo ""
echo "[2/4] Aplicando migraciones..."
python manage.py migrate --run-syncdb

# 3. Superusuario
echo ""
echo "[3/5] Creando superusuario (admin / admin)..."
python manage.py createsu

# 4. Roles
echo ""
echo "[4/5] Creando roles y permisos..."
python manage.py crear_roles

# 5. Datos de ejemplo
echo ""
echo "[5/5] Poblando datos de ejemplo..."
python manage.py poblar_datos

echo ""
echo "========================================"
echo "  Listo. Ejecuta el servidor con:"
echo "  python manage.py runserver"
echo "========================================"
