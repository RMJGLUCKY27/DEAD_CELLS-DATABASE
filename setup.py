import time
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DEAD_CELLS']

# Colecciones
weapons = db['weapons']
weapon_types = db['weapon_types']
tierlists = db['tierlists']

# Función para el efecto de escritura letra por letra
def escribir_lentamente(texto, delay=0.05):
    for letra in texto:
        print(letra, end='', flush=True)
        time.sleep(delay)
    print()  # Salto de línea al finalizar

# Interfaz decorativa
def interfaz_inicio():
    print("=" * 50)
    escribir_lentamente("               BIENVENIDO A LA TIER", delay=0.08)
    print("=" * 50)
    escribir_lentamente("          DEAD CELLS TIERLIST", delay=0.08)
    escribir_lentamente("               By Jose Rico", delay=0.08)
    print("=" * 50)
    time.sleep(1)
    print("\n")

# Función para agregar un arma
def agregar_arma():
    print("\n--- Agregar nueva arma ---")
    nombre = input("Nombre del arma: ")
    tipo = input("Tipo de arma: ")
    caracteristicas = input("Características: ")
    imagen_url = input("URL de la imagen: ")

    # Insertar en la base de datos de armas
    weapon = {
        "nombre": nombre,
        "tipo": tipo,
        "caracteristicas": caracteristicas,
        "imagen_url": imagen_url
    }
    weapons.insert_one(weapon)
    print(f"Arma '{nombre}' agregada con éxito.")

    # Asignar tierlist al arma
    asignar_tierlist_a_arma(nombre)

# Función para asignar una tierlist al arma
def asignar_tierlist_a_arma(arma_nombre):
    print("\n--- Asignar Tierlist ---")
    tierlist_existente = list(tierlists.find())

    if tierlist_existente:
        print("Selecciona una tierlist existente para asignar al arma:")
        for i, tierlist in enumerate(tierlist_existente, 1):
            print(f"{i}. Tier: {tierlist['tier']}")

        opcion = input("Ingrese el número de la tierlist (o 'n' para crear una nueva): ")
        if opcion.lower() != 'n':
            try:
                opcion = int(opcion)
                if 1 <= opcion <= len(tierlist_existente):
                    tierlist = tierlist_existente[opcion - 1]
                    tierlists.update_one(
                        {"_id": tierlist["_id"]},
                        {"$push": {"armas": weapons.find_one({"nombre": arma_nombre})["_id"]}}
                    )
                    print(f"Arma '{arma_nombre}' asignada a la tierlist '{tierlist['tier']}'.")
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        else:
            # Crear nueva tierlist si elige 'n'
            crear_tierlist(arma_nombre)
    else:
        # Si no hay tierlist, crear una nueva
        crear_tierlist(arma_nombre)

# Función para crear una tierlist y asignarla al arma
def crear_tierlist(arma_nombre):
    print("\n--- Crear nueva tierlist ---")
    tier = input("Nivel de la tierlist (S, A, B, C, D): ")
    tierlist = {
        "tier": tier,
        "armas": [weapons.find_one({"nombre": arma_nombre})["_id"]]
    }
    tierlists.insert_one(tierlist)
    print(f"Tierlist '{tier}' creada y arma '{arma_nombre}' asignada a ella.")

# Función para buscar un arma
def buscar_arma():
    print("\n--- Buscar arma ---")
    criterio = input("Buscar por nombre: ")
    arma = weapons.find_one({"nombre": criterio})
    if arma:
        print(f"\nNombre: {arma['nombre']}")
        print(f"Tipo: {arma['tipo']}")
        print(f"Características: {arma['caracteristicas']}")
        print(f"Imagen URL: {arma['imagen_url']}")
    else:
        print("Arma no encontrada.")

# Función para crear una tierlist
def crear_tierlist_menu():
    print("\n--- Crear nueva tierlist ---")
    tier = input("Nivel de la tierlist (S, A, B, C, D): ")
    nombres_armas = input("Ingrese los nombres de las armas separadas por comas: ").split(',')

    # Buscar armas por nombre
    armas_ids = []
    for nombre in nombres_armas:
        arma = weapons.find_one({"nombre": nombre.strip()})
        if arma:
            armas_ids.append(arma["_id"])
        else:
            print(f"Arma '{nombre.strip()}' no encontrada y no será incluida.")

    # Crear tierlist
    tierlist = {
        "tier": tier,
        "armas": armas_ids
    }
    tierlists.insert_one(tierlist)
    print(f"Tierlist '{tier}' creada con éxito.")

# Función para mostrar tierlists
def mostrar_tierlists():
    print("\n--- Mostrar tierlists ---")
    for tierlist in tierlists.find():
        print(f"\nTier: {tierlist['tier']}")
        for arma_id in tierlist['armas']:
            arma = weapons.find_one({"_id": arma_id})
            if arma:
                print(f"- {arma['nombre']} ({arma['tipo']})")

# Función para actualizar un arma
def actualizar_arma():
    print("\n--- Actualizar arma ---")
    nombre = input("Nombre del arma a actualizar: ")
    arma = weapons.find_one({"nombre": nombre})
    if arma:
        nuevo_tipo = input("Nuevo tipo de arma: ")
        nuevas_caracteristicas = input("Nuevas características: ")

        # Actualizar arma
        weapons.update_one(
            {"_id": arma["_id"]},
            {"$set": {"tipo": nuevo_tipo, "caracteristicas": nuevas_caracteristicas}}
        )
        print(f"Arma '{nombre}' actualizada con éxito.")
    else:
        print("Arma no encontrada.")

# Función para eliminar un arma
def eliminar_arma():
    print("\n--- Eliminar arma ---")
    nombre = input("Nombre del arma a eliminar: ")
    arma = weapons.find_one({"nombre": nombre})
    if arma:
        # Eliminar el arma de las tierlists
        tierlists.update_many({}, {"$pull": {"armas": arma["_id"]}})
        # Eliminar el arma de la colección
        weapons.delete_one({"_id": arma["_id"]})
        print(f"Arma '{nombre}' eliminada con éxito.")
    else:
        print("Arma no encontrada.")

# Menú principal
def menu():
    interfaz_inicio()
    while True:
        print("\nMenú Principal")
        print("1. Agregar arma")
        print("2. Buscar arma")
        print("3. Crear tierlist")
        print("4. Mostrar tierlists")
        print("5. Actualizar arma")
        print("6. Eliminar arma")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_arma()
        elif opcion == "2":
            buscar_arma()
        elif opcion == "3":
            crear_tierlist_menu()
        elif opcion == "4":
            mostrar_tierlists()
        elif opcion == "5":
            actualizar_arma()
        elif opcion == "6":
            eliminar_arma()
        elif opcion == "7":
            escribir_lentamente("Saliendo del programa... ¡Adiós!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
