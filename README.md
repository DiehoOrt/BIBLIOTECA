# NBiblioteca

Sistema de gestión de biblioteca desarrollado con Django 6. Permite administrar el inventario de libros, los alumnos, los préstamos y las multas por devolución tardía.

---

## Características

- **Alumnos** — registro, perfil, historial de préstamos y estado (activo / suspendido / inactivo)
- **Libros** — inventario con autores, categorías, portada y stock en tiempo real
- **Categorías** — clasificación de libros filtrable en el catálogo público
- **Préstamos** — registro y devolución con control de stock automático; estima multa antes de confirmar
- **Multas** — generación automática al devolver con retraso ($1.00/día); pago y anulación por rol
- **Catálogo público** — vista de tarjetas con portadas, filtro por categoría y búsqueda (sin login)
- **Reporte de morosos** — lista de alumnos con multas o préstamos vencidos

---

## Tecnologías

| Paquete | Versión |
|---|---|
| Python | 3.x |
| Django | 6.0.4 |
| Pillow | 12.2.0 |
| django-jazzmin | 3.0.4 |
| Bootstrap | 5.3.3 |
| Bootstrap Icons | 1.11.3 |
| Boxicons | 2.1.4 |

Base de datos: **SQLite** (desarrollo)

---

## Estructura del proyecto

```
NBiblioteca/
├── apps/
│   ├── alumnos/        # Gestión de alumnos
│   ├── libros/         # Libros, autores y categorías
│   ├── prestamos/      # Préstamos y devoluciones
│   ├── multas/         # Multas por retraso
│   └── management/     # Comandos personalizados
├── media/
│   └── portadas/       # Imágenes de portadas subidas
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
│   ├── base.html               # Base interna (con sidebar)
│   ├── base_catalogo.html      # Base pública (sin sidebar)
│   ├── dashboard.html
│   ├── components/
│   │   └── footer.html         # Footer del catálogo público
│   ├── alumnos/
│   ├── libros/
│   ├── prestamos/
│   └── multas/
├── NBiblioteca/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

---

## Instalación rápida con `build.sh`

El script `build.sh` automatiza los pasos de instalación. Antes de ejecutarlo necesitas tener el entorno virtual **creado y activo**.

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd NBiblioteca
```

### 2. Crear y activar el entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

> Verifica que el entorno esté activo: el prompt debe mostrar `(venv)` al inicio.

### 3. Ejecutar el script

```bash
bash build.sh
```

El script realiza automáticamente:

| Paso | Acción |
|---|---|
| 1/5 | Instala dependencias desde `requirements.txt` |
| 2/5 | Aplica las migraciones de base de datos |
| 3/5 | Crea el superusuario (`admin` / `admin`) |
| 4/5 | Crea el grupo y permisos de Bibliotecario |
| 5/5 | Puebla la base de datos con datos de ejemplo |

### 4. Iniciar el servidor

```bash
python manage.py runserver
```

Accede en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Instalación manual (paso a paso)

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd NBiblioteca
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> El archivo `requirements.txt` en la raíz del proyecto incluye todas las dependencias con sus versiones exactas.

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
# Opción A — interactivo
python manage.py createsuperuser

# Opción B — comando personalizado (usuario: admin / contraseña: admin)
python manage.py createsu
```

### 6. Poblar datos de ejemplo *(opcional)*

```bash
python manage.py poblar_datos
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Rutas principales

| URL | Descripción |
|---|---|
| `/` | Dashboard principal |
| `/login/` | Inicio de sesión |
| `/catalogo/` | Catálogo público (sin login) |
| `/alumnos/` | Lista de alumnos |
| `/libros/` | Lista de libros |
| `/libros/categorias/` | Gestión de categorías |
| `/libros/autores/` | Gestión de autores |
| `/prestamos/` | Lista de préstamos |
| `/prestamos/<id>/devolver/` | Confirmar devolución de un préstamo |
| `/multas/` | Lista de multas |
| `/reportes/morosos/` | Reporte de morosos |
| `/admin/` | Panel de administración Django |

---

## Roles y permisos

El sistema tiene dos roles diferenciados:

| | Bibliotecario | Administrador |
|---|---|---|
| Alumnos, libros, autores, categorías | ✅ | ✅ |
| Registrar y devolver préstamos | ✅ | ✅ |
| Ver y pagar multas | ✅ | ✅ |
| Anular multas | ❌ | ✅ |
| Panel de administración `/admin/` | ❌ | ✅ |
| Crear usuarios / asignar permisos | ❌ | ✅ |

### Crear el grupo Bibliotecario

```bash
python manage.py crear_roles
```

### Asignar el rol a un usuario

1. Ingresa al panel admin: `/admin/`
2. Ve a **Autenticación → Usuarios → [usuario]**
3. En **Grupos** selecciona `Bibliotecario`
4. Asegúrate de que tenga `is_staff = False` e `is_superuser = False`
5. Guarda

> Un Bibliotecario con `is_staff=False` no puede acceder a `/admin/`. El enlace al Panel Admin en el menú lateral solo es visible para superusuarios.

---

## Lógica de negocio

- Un alumno solo puede recibir préstamos si su estado es **Activo** y no tiene **multas pendientes**.
- Al registrar un préstamo el stock disponible del libro se **descuenta automáticamente**.
- Al devolver un libro el stock se **incrementa automáticamente**.
- Si la devolución es tardía se genera una **multa automática** de $1.00 por día de retraso.
- No es posible eliminar un alumno o libro que tenga préstamos registrados.

---

## Flujo de trabajo (Git)

### Ramas principales

| Rama | Propósito |
|---|---|
| `main` | Código estable, listo para entregar |
| `develop` | Integración de cambios antes de pasar a `main` |
| `avance-50` | Versión de presentación al 50% |

### Ramas de trabajo

- `feature/nombre` — para agregar funcionalidad nueva
- `fix/nombre` — para corregir bugs

### Reglas

- Siempre partir de `develop` para crear una rama nueva
- Los Pull Requests van hacia `develop`, nunca directo a `main`
- Solo el administrador hace merge de `develop` a `main`

### Ejemplo para colaboradores

```bash
# 1. Actualizar develop local
git checkout develop
git pull origin develop

# 2. Crear rama para tu tarea
git checkout -b feature/mi-funcionalidad

# 3. Trabajar, hacer commits
git add .
git commit -m "descripción del cambio"

# 4. Subir la rama y abrir Pull Request hacia develop
git push origin feature/mi-funcionalidad
```

---

## Variables de entorno recomendadas para producción

Antes de desplegar en producción edita `settings.py`:

```python
DEBUG = False
SECRET_KEY = '<clave-secreta-aleatoria>'
ALLOWED_HOSTS = ['tu-dominio.com']
```
