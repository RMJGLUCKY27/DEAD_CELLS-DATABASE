import json
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Crear la base de datos DEAD_CELLS
db = client['DEAD_CELLS']

# Crear colecciones
weapons = db['weapons']
weapon_types = db['weapon_types']
tierlists = db['tierlists']

# Función para cargar datos desde el archivo JSON
def cargar_documentos_desde_json(archivo):
    try:
        with open(archivo, 'r') as file:
            # Cargar el contenido completo del archivo JSON
            datos = json.load(file)
            
            # Imprimir para verificar la estructura de los datos
            print("Contenido cargado desde el archivo JSON:")
            print(json.dumps(datos, indent=4))  # Imprime el contenido con formato legible
            
            # Verificar e insertar datos en la colección 'weapons'
            if 'weapons' in datos and isinstance(datos['weapons'], list) and datos['weapons']:
                weapons.insert_many(datos['weapons'])
                print(f"Datos de 'weapons' cargados correctamente.")
            else:
                print("No se encontraron datos válidos para 'weapons'.")
            
            # Verificar e insertar datos en la colección 'tierlists'
            if 'tierlists' in datos and isinstance(datos['tierlists'], list) and datos['tierlists']:
                tierlists.insert_many(datos['tierlists'])
                print(f"Datos de 'tierlists' cargados correctamente.")
            else:
                print("No se encontraron datos válidos para 'tierlists'.")
            
            # Verificar e insertar datos en la colección 'weapon_types'
            if 'weapon_types' in datos and isinstance(datos['weapon_types'], list) and datos['weapon_types']:
                weapon_types.insert_many(datos['weapon_types'])
                print(f"Datos de 'weapon_types' cargados correctamente.")
            else:
                print("No se encontraron datos válidos para 'weapon_types'.")
                
    except Exception as e:
        print(f"Error al cargar los datos desde el archivo {archivo}: {e}")

# Llamada a la función para cargar los datos desde el archivo JSON
cargar_documentos_desde_json('initial_data.json')
