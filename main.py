import sqlite3

def crear_bd():
    conexion = sqlite3.connect("tareas.db")

    conexion.execute("PRAGMA foreign_keys = ON;")
    
    cursor = conexion.cursor()

    try:
        cursor.execute('''CREATE TABLE categoria(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo VARCHAR(50) UNIQUE
                    )''')
    except sqlite3.OperationalError:
        print("La tabla 'categoria' ya existe")
    else:
        print("La tabla 'categoria' ha sido creada correctamente")

    try:
        cursor.execute('''CREATE TABLE tarea(
                            id_tarea INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre VARCHAR(100) UNIQUE,
                            comentarios VARCHAR(200),
                            id_categoria INTEGER,
                            FOREIGN KEY (id_categoria) REFERENCES categoria(id)
                    )''')
    except sqlite3.OperationalError:
        print("La tabla 'tarea' ya existe")
    else:
        print("La tabla 'tarea' ha sido creada correctamente")


    conexion.close()

def obtener_tareas():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    
    # Eliminaré tareas usando el ID
    tareas = cursor.execute('''SELECT t.id_tarea, t.nombre, t.comentarios, c.titulo FROM tarea t
                            JOIN categoria c ON t.id_categoria = c.id''').fetchall()
    
    conexion.close()

    return tareas

def obtener_categorias():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()

    categorias = cursor.execute("SELECT id, titulo FROM categoria").fetchall()

    conexion.close()

    return categorias

def nueva_categoria(nombre_categoria):
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()

    try:
        cursor.execute(f'''INSERT INTO categoria(titulo) VALUES('{nombre_categoria.capitalize()}')''')
        conexion.commit()
    except sqlite3.IntegrityError:
        print(f"La categoria '{nombre_categoria.capitalize()}' ya existe")
    else:
        conexion.close()

def nueva_tarea():
    tarea = input("Tarea que quieres añadir: ")
    comentarios = input("Comentarios de la tarea: ")
    categoria = obtener_categorias()

    conexion = sqlite3.connect("tareas.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()

    print("\nEstas son las categorias junto con su ID: ")
    for c in categoria:
        print(f"Categoria: {c[1]}. ID = {c[0]}")

    print('''Escribe el ID de la categoria a la que quieres añadir tu tarea. 
          Si quieres una nueva categoría pon una X en el ID y crea la nueva categoría''')
    id_cat = input("ID: ")

    try:
        cursor.execute(f"INSERT INTO tarea(nombre, comentarios, id_categoria) VALUES('{tarea}', '{comentarios}', '{id_cat}')")
        conexion.commit()
        print("Tarea añadida correctamente!!")
    except sqlite3.IntegrityError:
        print("El ID que has puesto no existe o la tarea ya está en la lista")
    else:
        conexion.close()

def mostrar_tareas():
    tareas_pendientes =  obtener_tareas()
    
    if tareas_pendientes is None:
        print("No tienes tareas pendientes")
    else:
        print("Tareas pendientes: ")
        for tarea in tareas_pendientes:
            if tarea[2] is None:
                print(f"{tarea[1]} (id={tarea[0]}) - [{tarea[3]}]")
            else:
                print(f"{tarea[1]} (id={tarea[0]}) - {tarea[2]} [{tarea[3]}]")  

def eliminar_tarea(): # testearla
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()

    print("Vamos a eliminar una tarea. Escribe el ID de la tarea que quieras eliminar.")
    mostrar_tareas()
    id_eliminar = int(input("ID de la tarea > "))

    print(f"Estas seguro que quieres eliminar la tarea con ID {id_eliminar}? s/n")
    confirmacion = input("S/n > ").lower()

    if confirmacion != "s":
        return
    
    try:
        cursor.execute("DELETE FROM tarea WHERE id_tarea='?'", id_eliminar)
        conexion.commit()
    except sqlite3.ProgrammingError:
        print("El ID introducido no está en la lista")
    else:
        conexion.close()

def mostrar_tareas_por_categoria(): # testearla
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()

    print("Dispones de las siguientes categorías: ")
    categorias = cursor.execute("SELECT id, titulo FROM categoria").fetchall()
    for c in categorias:
        print(f"{c[0]} - {c[1]}")

    try:
        id_categoria = int(input("\nIntroduce el ID de la categoria: "))
    except:
        print("ID no valido")
        conexion.close()
        return
    
    cursor.execute(f"SELECT id_tarea, nombre, comentarios FROM tarea t JOIN categoria c ON t.id_categoria = c.id WHERE c.id = '{id_categoria}'")
    tareas_por_categoria = cursor.fetchall()

    if len(tareas_por_categoria) == 0:
        print(f"No hay tareas para la categoría con ID = {id_categoria}")
    else:
        for tarea in tareas_por_categoria:
            print(f"{tarea[1]} ({tarea[0]}) - ({tarea[2]})")

    conexion.close()

def menu():
    print('''\nOpciones
    1. Ver todas las tareas pendientes
    2. Añadir una nueva tarea
    3. Eliminar una tarea
    4. Mostrar las tareas de una categoría
    5. Añadir una nueva categoría
    6. Salir''')

while True:
    menu()
    opcion = input("Elige la opcion que deseas> ")
    print()

    if opcion == "1":
        mostrar_tareas()
    
    elif opcion == "2":
        nueva_tarea()

    elif opcion == "3":
        eliminar_tarea()

    elif opcion == "4":
        mostrar_tareas_por_categoria()
    
    elif opcion == "5":
        nueva = input("Título de la nueva categoria que quieres añadir: ")
        nueva_categoria(nueva)

    elif opcion == "6":
        print("Hasta la próxima!!!")
        break

    else:
        print("Opción no válida")

