from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta
from apps.alumnos.models import Alumno
from apps.libros.models import Autor, Categoria, Libro, LibroAutor, LibroCategoria
from apps.prestamos.models import Prestamo
from apps.multas.models import Multa


AUTORES = [
    ("Antoine",     "Saint-Exupéry"),
    ("Jinho",       "Ko"),
    ("Charles",     "Severance"),
    ("Robert C.",   "Martin"),
    ("Gege",        "Akutami"),
    ("J.K.",        "Rowling"),
    ("Dennis G.",   "Zill"),
    ("Richard P.",  "Feynman"),
    ("Travis",      "TurtleMe"),
    ("Kilian",      "Jornet"),
    ("Papa",        "Francisco"),
    ("Gabriel",     "García Márquez"),
    ("Sun",         "Tzu"),
    ("Yuval Noah",  "Harari"),
    ("James",       "Clear"),
    ("George",      "Orwell"),
    ("Robert T.",   "Kiyosaki"),
    ("Fyodor",      "Dostoievski"),
    ("Carl",        "Sagan"),
]

CATEGORIAS = [
    ("Novela",      "Obras de ficción narrativa de largo aliento"),
    ("Ciencia",     "Divulgación científica y tecnología"),
    ("Filosofía",   "Pensamiento filosófico y ensayo"),
    ("Historia",    "Libros de historia universal y regional"),
    ("Informática", "Programación, redes y sistemas"),
    ("Manga",       "Cómics y novelas gráficas japonesas y coreanas"),
    ("Fantasía",    "Obras de fantasía y ciencia ficción"),
    ("Finanzas",    "Economía personal, inversión y finanzas"),
    ("Matemática",  "Álgebra, cálculo y matemática aplicada"),
    ("Autoayuda",   "Desarrollo personal y hábitos"),
    ("Religión",    "Teología, espiritualidad y textos religiosos"),
]

# (titulo, isbn, anio, cantidad, autores_apellidos, categorias, descripcion, portada)
LIBROS = [
    (
        "El Principito",
        "978-0156012195", 1943, 4,
        ["Saint-Exupéry"], ["Novela", "Filosofía"],
        "Un aviador varado en el desierto conoce a un niño de otro planeta. Fábula poética sobre la amistad y lo que realmente importa en la vida.",
        "portadas/Plibro1.png",
    ),
    (
        "Jack Frost",
        "978-0759531376", 2007, 3,
        ["Ko"], ["Manga", "Fantasía"],
        "En el oscuro Instituto Amityville, Noh-A Hyun descubre que los estudiantes son atacados por seres sobrenaturales. Thriller de horror con atmósfera única.",
        "portadas/Plibro2.png",
    ),
    (
        "Python para Todos",
        "978-9999999991", 2016, 5,
        ["Severance"], ["Informática"],
        "Introducción a la programación con Python orientada a principiantes. Cubre estructuras de datos, funciones y conexión con bases de datos.",
        "portadas/plibro3.png",
    ),
    (
        "Principios SOLID",
        "978-0135974445", 2018, 3,
        ["Martin"], ["Informática"],
        "Guía esencial sobre los cinco principios de diseño orientado a objetos para escribir código mantenible, flexible y escalable.",
        "portadas/plibro4.png",
    ),
    (
        "Jujutsu Kaisen Vol. 29",
        "978-1974743476", 2024, 4,
        ["Akutami"], ["Manga"],
        "Volumen 29 del manga de acción sobrenatural. Los hechiceros enfrentan el clímax de su batalla más devastadora contra las maldiciones de grado especial.",
        "portadas/plibro5.png",
    ),
    (
        "Harry Potter y la Piedra Filosofal",
        "978-8478884452", 1997, 5,
        ["Rowling"], ["Novela", "Fantasía"],
        "Un niño descubre que es mago el día de su undécimo cumpleaños y comienza su educación en Hogwarts. El inicio de una saga mágica ya clásica.",
        "portadas/plibro6.png",
    ),
    (
        "Ecuaciones Diferenciales",
        "978-6071503091", 2015, 4,
        ["Zill"], ["Ciencia", "Matemática"],
        "Texto universitario de referencia sobre ecuaciones diferenciales ordinarias y parciales con aplicaciones en ingeniería y ciencias aplicadas.",
        "portadas/plibro7.png",
    ),
    (
        "Física Cuántica",
        "978-9876543215", 2018, 3,
        ["Feynman"], ["Ciencia"],
        "Exploración de los principios de la mecánica cuántica, desde la dualidad onda-partícula hasta la entrelazación y sus implicaciones en la física moderna.",
        "portadas/plibro8.png",
    ),
    (
        "The Beginning After the End Vol. 11",
        "978-9999999992", 2023, 3,
        ["TurtleMe"], ["Novela", "Fantasía"],
        "Arthur Leywin avanza en un mundo de magia y peligro, enfrentando amenazas que pondrán a prueba sus límites. Clímax del arco más oscuro de la saga.",
        "portadas/plibro9.png",
    ),
    (
        "Correr o Morir",
        "978-8494001109", 2012, 2,
        ["Jornet"], ["Autoayuda"],
        "El ultramaratonista Kilian Jornet narra sus hazañas en las carreras de montaña más exigentes del mundo. Un relato de superación y pasión extrema.",
        "portadas/plibro10.jpg",
    ),
    (
        "Laudato Si — Encíclica",
        "978-8490553411", 2015, 3,
        ["Francisco"], ["Religión", "Filosofía"],
        "Carta encíclica del Papa Francisco sobre el cuidado de la casa común. Reflexiona sobre la crisis ecológica desde una perspectiva ética y espiritual.",
        "portadas/plibro11.png",
    ),
    (
        "Cien Años de Soledad",
        "978-0307474728", 1967, 5,
        ["García Márquez"], ["Novela"],
        "La saga de la familia Buendía en el mítico Macondo. Obra cumbre del realismo mágico que retrata el ciclo de la historia latinoamericana.",
        "portadas/plibro12.png",
    ),
    (
        "El Arte de la Guerra",
        "978-8491392033", 2015, 4,
        ["Tzu"], ["Filosofía", "Historia"],
        "Tratado militar del estratega chino Sun Tzu. Sus principios sobre estrategia, liderazgo y conflicto han sido aplicados durante siglos en distintos ámbitos.",
        "portadas/plibro13.png",
    ),
    (
        "Sapiens: De animales a dioses",
        "978-8499926223", 2011, 4,
        ["Harari"], ["Historia", "Ciencia"],
        "Un recorrido por la historia de la humanidad desde el Homo Sapiens hasta la era digital. Desafía las nociones convencionales sobre progreso y poder.",
        "portadas/plibro14.png",
    ),
    (
        "Harry Potter y la Cámara Secreta",
        "978-8478884469", 1998, 5,
        ["Rowling"], ["Novela", "Fantasía"],
        "El segundo año de Harry en Hogwarts trae una amenaza misteriosa que petrifica estudiantes. La leyenda de la Cámara Secreta cobra vida.",
        "portadas/plibro15.png",
    ),
    (
        "Hábitos Atómicos",
        "978-8418118227", 2018, 4,
        ["Clear"], ["Autoayuda", "Filosofía"],
        "Sistema práctico para construir buenos hábitos y eliminar los malos, basado en la ciencia del comportamiento con estrategias aplicables desde el primer día.",
        "portadas/plibro16.png",
    ),
    (
        "1984",
        "978-0451524935", 1949, 4,
        ["Orwell"], ["Novela", "Filosofía"],
        "En el totalitario Oceanía, Winston Smith intenta resistir al Gran Hermano. Distopía visionaria sobre el control, la vigilancia y la destrucción del pensamiento libre.",
        "portadas/plibro17.png",
    ),
    (
        "Padre Rico, Padre Pobre",
        "978-9584248213", 1997, 4,
        ["Kiyosaki"], ["Finanzas"],
        "Contrasta la mentalidad financiera de dos padres para enseñar educación económica. Un clásico que cambia la perspectiva sobre el dinero y los activos.",
        "portadas/plibro18.png",
    ),
    (
        "Crimen y Castigo",
        "978-8491050568", 1866, 3,
        ["Dostoievski"], ["Novela", "Filosofía"],
        "Raskolnikov comete un crimen creyéndose superior a la ley. Profundo análisis psicológico sobre la culpa, la redención y la moral humana.",
        "portadas/plibro19.png",
    ),
    (
        "Cosmos",
        "978-8484326243", 1980, 3,
        ["Sagan"], ["Ciencia", "Historia"],
        "Carl Sagan lleva al lector en un viaje por el universo y la historia de la ciencia. Poético, riguroso y profundamente inspirador.",
        "portadas/plibro20.png",
    ),
]

# (nombre, apellido, carnet, email, estado)
ALUMNOS = [
    # activos 2021
    ("Carlos",    "Martínez",   "2021-001", "carlos.martinez@unicaes.edu.sv",    "activo"),
    ("María",     "López",      "2021-002", "maria.lopez@unicaes.edu.sv",        "activo"),
    ("José",      "Hernández",  "2021-003", "jose.hernandez@unicaes.edu.sv",     "activo"),
    ("Ana",       "García",     "2021-004", "ana.garcia@unicaes.edu.sv",         "activo"),
    ("Luis",      "Rodríguez",  "2021-005", "luis.rodriguez@unicaes.edu.sv",     "activo"),
    ("Sofía",     "Pérez",      "2021-006", "sofia.perez@unicaes.edu.sv",        "activo"),
    ("Diego",     "Ramírez",    "2021-007", "diego.ramirez@unicaes.edu.sv",      "activo"),
    ("Valentina", "Torres",     "2021-008", "valentina.torres@unicaes.edu.sv",   "activo"),
    # suspendidos
    ("Andrés",    "Flores",     "2021-009", "andres.flores@unicaes.edu.sv",      "suspendido"),
    ("Camila",    "Rivera",     "2021-010", "camila.rivera@unicaes.edu.sv",      "suspendido"),
    # inactivos 2020
    ("Ricardo",   "Morales",    "2020-001", "ricardo.morales@unicaes.edu.sv",    "inactivo"),
    ("Paola",     "Jiménez",    "2020-002", "paola.jimenez@unicaes.edu.sv",      "inactivo"),
    # activos 2022
    ("Fernando",  "Castillo",   "2022-001", "fernando.castillo@unicaes.edu.sv",  "activo"),
    ("Daniela",   "Mendoza",    "2022-002", "daniela.mendoza@unicaes.edu.sv",    "activo"),
    ("Miguel",    "Vargas",     "2022-003", "miguel.vargas@unicaes.edu.sv",      "activo"),
    ("Patricia",  "Velásquez",  "2022-004", "patricia.velasquez@unicaes.edu.sv", "activo"),
    ("Eduardo",   "Salazar",    "2022-005", "eduardo.salazar@unicaes.edu.sv",    "activo"),
    # activos 2023
    ("Alejandra", "Núñez",      "2023-001", "alejandra.nunez@unicaes.edu.sv",    "activo"),
    ("Roberto",   "Escobar",    "2023-002", "roberto.escobar@unicaes.edu.sv",    "activo"),
    ("Gabriela",  "Contreras",  "2023-003", "gabriela.contreras@unicaes.edu.sv", "activo"),
    ("Felipe",    "Herrera",    "2023-004", "felipe.herrera@unicaes.edu.sv",     "activo"),
    ("Natalia",   "Aguilar",    "2023-005", "natalia.aguilar@unicaes.edu.sv",    "activo"),
    # suspendidos adicionales
    ("Sebastián", "Reyes",      "2021-011", "sebastian.reyes@unicaes.edu.sv",    "suspendido"),
    ("Lorena",    "Castro",     "2021-012", "lorena.castro@unicaes.edu.sv",      "suspendido"),
    # inactivo antiguo
    ("Manuel",    "Ortega",     "2019-001", "manuel.ortega@unicaes.edu.sv",      "inactivo"),
]


class Command(BaseCommand):
    help = "Pobla la base de datos con datos de ejemplo en diferentes estados"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando carga de datos...")

        with transaction.atomic():
            autores = self._crear_autores()
            cats    = self._crear_categorias()
            libros  = self._crear_libros(autores, cats)
            alumnos = self._crear_alumnos()
            self._crear_prestamos(alumnos, libros)

        self.stdout.write(self.style.SUCCESS("Datos cargados correctamente."))

    # ------------------------------------------------------------------ #

    def _crear_autores(self):
        mapa = {}
        for nombre, apellido in AUTORES:
            obj, created = Autor.objects.get_or_create(nombre=nombre, apellido=apellido)
            mapa[apellido] = obj
            if created:
                self.stdout.write(f"  Autor creado: {obj}")
        return mapa

    def _crear_categorias(self):
        mapa = {}
        for nombre, desc in CATEGORIAS:
            obj, created = Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
            mapa[nombre] = obj
            if created:
                self.stdout.write(f"  Categoría creada: {obj}")
        return mapa

    def _crear_libros(self, autores, cats):
        libros = []
        for titulo, isbn, anio, cantidad, apellidos_autores, nombres_cats, descripcion, portada_file in LIBROS:
            libro, created = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "titulo":              titulo,
                    "anio_publicacion":    anio,
                    "cantidad_total":      cantidad,
                    "cantidad_disponible": cantidad,
                    "descripcion":         descripcion,
                    "portada":             portada_file,
                },
            )
            if created:
                self.stdout.write(f"  Libro creado: {libro}")
                for apellido in apellidos_autores:
                    if apellido in autores:
                        LibroAutor.objects.get_or_create(libro=libro, autor=autores[apellido])
                for cat_nombre in nombres_cats:
                    if cat_nombre in cats:
                        LibroCategoria.objects.get_or_create(libro=libro, categoria=cats[cat_nombre])
            else:
                libro.descripcion = descripcion
                libro.portada     = portada_file
                libro.save(update_fields=["descripcion", "portada"])
                self.stdout.write(f"  Libro actualizado (desc/portada): {libro}")
            libros.append(libro)
        return libros

    def _crear_alumnos(self):
        alumnos = []
        for nombre, apellido, carnet, email, estado in ALUMNOS:
            obj, created = Alumno.objects.get_or_create(
                carnet=carnet,
                defaults={
                    "nombre":   nombre,
                    "apellido": apellido,
                    "email":    email,
                    "estado":   estado,
                },
            )
            if created:
                self.stdout.write(f"  Alumno creado: {obj}")
            alumnos.append(obj)
        return alumnos

    def _crear_prestamos(self, alumnos, libros):
        hoy = date.today()

        # (alumno_idx, libro_idx, dias_atras, dias_esperados, devuelto_en_dias, estado_multa)
        escenarios = [
            # --- ACTIVOS a tiempo ---
            (0,  0,  2,  15, None, None),
            (1,  5,  4,  15, None, None),
            (2,  11, 1,  15, None, None),
            (3,  15, 6,  15, None, None),
            (4,  3,  3,  15, None, None),
            (12, 7,  5,  15, None, None),
            (17, 13, 2,  15, None, None),
            (18, 17, 7,  15, None, None),
            # --- ACTIVOS vencidos ---
            (5,  1,  20, 15, None, None),
            (6,  6,  18, 15, None, None),
            (8,  4,  25, 15, None, None),
            (22, 9,  30, 15, None, None),
            (13, 14, 22, 15, None, None),
            # --- DEVUELTOS a tiempo ---
            (0,  2,  30, 15, 12,   None),
            (1,  10, 25, 15, 10,   None),
            (2,  8,  40, 15, 13,   None),
            (4,  19, 35, 15, 14,   None),
            (7,  0,  22, 15,  7,   None),
            (12, 12, 45, 15, 11,   None),
            (14, 18, 28, 15,  9,   None),
            (15, 5,  50, 15, 12,   None),
            (20, 3,  15, 15,  6,   None),
            (19, 16, 32, 15, 14,   None),
            # --- DEVUELTOS tardíos → multa pendiente ---
            (4,  6,  35, 15, 20, "pendiente"),
            (5,  8,  50, 15, 25, "pendiente"),
            (6,  10, 45, 15, 22, "pendiente"),
            (7,  12, 60, 15, 30, "pendiente"),
            (9,  15, 40, 15, 21, "pendiente"),
            (23, 1,  55, 15, 27, "pendiente"),
            # --- DEVUELTOS tardíos → multa pagada ---
            (0,  14, 90, 15, 25, "pagada"),
            (1,  17, 80, 15, 22, "pagada"),
            (2,  5,  70, 15, 20, "pagada"),
            (3,  0,  65, 15, 18, "pagada"),
            (12, 19, 75, 15, 24, "pagada"),
            (16, 11, 85, 15, 28, "pagada"),
            # --- DEVUELTOS tardíos → multa anulada ---
            (9,  2,  55, 15, 23, "anulada"),
            (10, 4,  48, 15, 21, "anulada"),
            (11, 7,  60, 15, 26, "anulada"),
            (24, 13, 52, 15, 24, "anulada"),
        ]

        for alumno_i, libro_i, dias_atras, dias_esperados, devuelto_en, estado_multa in escenarios:
            alumno = alumnos[alumno_i]
            libro  = libros[libro_i]

            fecha_prestamo   = hoy - timedelta(days=dias_atras)
            fecha_esperada   = fecha_prestamo + timedelta(days=dias_esperados)
            fecha_devolucion = (fecha_prestamo + timedelta(days=devuelto_en)) if devuelto_en else None

            if fecha_devolucion:
                estado = Prestamo.ESTADO_DEVUELTO
            elif hoy > fecha_esperada:
                estado = Prestamo.ESTADO_VENCIDO
            else:
                estado = Prestamo.ESTADO_ACTIVO

            existe = Prestamo.objects.filter(
                alumno=alumno, libro=libro, fecha_prestamo=fecha_prestamo
            ).exists()
            if existe:
                continue

            prestamo = Prestamo(
                alumno=alumno,
                libro=libro,
                fecha_devolucion_esperada=fecha_esperada,
                fecha_devolucion_real=fecha_devolucion,
                estado=estado,
            )
            prestamo.save()
            Prestamo.objects.filter(pk=prestamo.pk).update(fecha_prestamo=fecha_prestamo)

            if estado in (Prestamo.ESTADO_ACTIVO, Prestamo.ESTADO_VENCIDO):
                libro.cantidad_disponible = max(0, libro.cantidad_disponible - 1)
                libro.save(update_fields=["cantidad_disponible"])

            if fecha_devolucion and fecha_devolucion > fecha_esperada:
                dias_retraso = (fecha_devolucion - fecha_esperada).days
                multa, created = Multa.objects.get_or_create(
                    prestamo=prestamo,
                    defaults={
                        "monto":  round(dias_retraso * 1.00, 2),
                        "motivo": f"Devolución tardía: {dias_retraso} día(s) de retraso",
                        "estado": estado_multa or "pendiente",
                    },
                )
                if not created and estado_multa:
                    multa.estado = estado_multa
                    if estado_multa == "pagada":
                        multa.fecha_pago = fecha_devolucion + timedelta(days=2)
                    multa.save()

            self.stdout.write(f"  Préstamo: {alumno} | {libro} | {estado}")
