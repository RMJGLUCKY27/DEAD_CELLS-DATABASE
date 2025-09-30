## Resumen para README - DEAD_CELLS-DATABASE

Este proyecto es un sistema de gestión de base de datos para armas del videojuego Dead Cells, que permite crear, administrar y visualizar tierlists de armas [1](#0-0) . El sistema utiliza MongoDB como base de datos y está compuesto por tres componentes principales que trabajan de forma independiente.

## Componentes del Sistema

### 1. Inicialización de Base de Datos (`cargainicial.py`)
Carga los datos iniciales desde un archivo JSON a las colecciones de MongoDB [2](#0-1) . Establece las tres colecciones principales: `weapons`, `weapon_types` y `tierlists` [3](#0-2) .

### 2. Interfaz de Gestión CLI (`setup.py`)
Proporciona un menú interactivo para administrar las armas y tierlists con las siguientes funcionalidades [4](#0-3) :
- Agregar nuevas armas
- Buscar armas existentes
- Crear y gestionar tierlists
- Actualizar y eliminar armas

### 3. Visualización de Tierlists (`app.py`)
Genera visualizaciones gráficas de las tierlists usando matplotlib, mostrando las armas organizadas por tiers (S, A, B, C, D) con sus respectivas imágenes [5](#0-4) .

## Estructura de Datos

El sistema maneja tres tipos de documentos principales:
- **Armas**: Contienen nombre, tipo, características e imagen_url [6](#0-5) 
- **Tierlists**: Organizan las armas por niveles de tier [7](#0-6) 
- **Tipos de Arma**: Categorizan las armas por tipo [8](#0-7) 

## Requisitos
- MongoDB (localhost:27017)
- Python con librerías: pymongo, matplotlib, requests, PIL

## Uso
1. Ejecutar `cargainicial.py` para inicializar la base de datos
2. Usar `setup.py` para gestión interactiva de datos
3. Ejecutar `app.py` para visualizar tierlists

**Notes**

El sistema está diseñado con arquitectura modular donde cada componente puede ejecutarse independientemente después de la inicialización. La conexión a MongoDB sigue un patrón consistente en los tres archivos [9](#0-8) . El proyecto incluye manejo de errores y validación de datos para garantizar la integridad de la información.

Wiki pages you might want to explore:
- [System Components (RMJGLUCKY27/DEAD_CELLS-DATABASE)](/wiki/RMJGLUCKY27/DEAD_CELLS-DATABASE#3)

### Citations

**File:** setup.py (L1-11)
```python
import time
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DEAD_CELLS']

# Colecciones
weapons = db['weapons']
weapon_types = db['weapon_types']
tierlists = db['tierlists']
```

**File:** setup.py (L184-217)
```python
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
```

**File:** cargainicial.py (L10-13)
```python
# Crear colecciones
weapons = db['weapons']
weapon_types = db['weapon_types']
tierlists = db['tierlists']
```

**File:** cargainicial.py (L16-51)
```python
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
```

**File:** app.py (L48-97)
```python
def mostrar_tierlist():
    armas_por_tier = obtener_armas_por_tiers()
    tiers = ['S', 'A', 'B', 'C', 'D']
    colores = {
        'S': rgb_color((255, 102, 102)),  # Rojo pastel
        'A': rgb_color((255, 178, 102)),  # Naranja suave
        'B': rgb_color((102, 255, 178)),  # Verde agua
        'C': rgb_color((102, 178, 255)),  # Azul claro
        'D': rgb_color((204, 153, 255)),  # Morado pastel
    }

    # Configurar el gráfico
    fig, ax = plt.subplots(len(tiers), 1, figsize=(12, 3 * len(tiers)))
    if len(tiers) == 1:
        ax = [ax]

    max_por_fila = 10  # Máximo de armas por fila

    for i, tier in enumerate(tiers):
        armas = armas_por_tier[tier]
        filas = -(-len(armas) // max_por_fila)  # Calcular número de filas necesarias
        ax[i].set_facecolor(colores[tier])  # Fondo de color según el tier
        ax[i].set_xlim(0, max_por_fila + 1)  # Ajustar el ancho para múltiples filas
        ax[i].set_ylim(0, filas * 1.5)  # Ajustar el alto según el número de filas
        ax[i].axis('off')

        # Agregar título del tier
        ax[i].text(-0.5, filas * 1.25, f"Tier {tier}", fontsize=16, va='center', ha='center', color='black', bbox=dict(facecolor=colores[tier], edgecolor='none'))

        # Mostrar las imágenes de las armas en múltiples filas
        for j, arma in enumerate(armas):
            fila_actual = j // max_por_fila
            columna_actual = j % max_por_fila
            x_pos = columna_actual + 1
            y_pos = filas - fila_actual - 1  # Invertir para que la primera fila esté arriba

            img = obtener_imagen(arma['imagen_url'])
            if img:
                ax[i].imshow(img, extent=[x_pos - 0.4, x_pos + 0.4, y_pos + 0.2, y_pos + 1])  # Posicionar la imagen

            # Ajustar el nombre debajo de la imagen con texto envuelto
            nombre_ajustado = textwrap.fill(arma['nombre'], width=10)  # Limitar a 10 caracteres por línea
            ax[i].text(x_pos, y_pos - 0.1, nombre_ajustado, fontsize=8, va='top', ha='center', color='black')

    plt.tight_layout()
    plt.show()

# Ejecutar la visualización
if __name__ == "__main__":
    mostrar_tierlist()
```

**File:** initial_data.json (L2-31)
```json
    "weapons": [
        {
            "weapon_id": 1,
            "nombre": "Espada de Cristal",
            "tipo_id": 1,
            "caracteristicas": "Espada de alto daño que atraviesa a los enemigos.",
            "imagen_url": "https://static.dead-cells.com/espada_cristal.png"
        },
        {
            "weapon_id": 2,
            "nombre": "Martillo de Guerra",
            "tipo_id": 2,
            "caracteristicas": "Martillo pesado que inflige gran daño en área.",
            "imagen_url": "https://static.dead-cells.com/martillo_guerra.png"
        },
        {
            "weapon_id": 3,
            "nombre": "Lanza de Fuego",
            "tipo_id": 3,
            "caracteristicas": "Lanza que inflige daño de fuego en el impacto.",
            "imagen_url": "https://static.dead-cells.com/lanza_fuego.png"
        },
        {
            "weapon_id": 4,
            "nombre": "Arco de Hierro",
            "tipo_id": 4,
            "caracteristicas": "Arco que dispara flechas a larga distancia con alta precisión.",
            "imagen_url": "https://static.dead-cells.com/arco_hierro.png"
        }
    ],
```

**File:** initial_data.json (L32-53)
```json
    "tierlists": [
        {
            "tierlist_id": 1,
            "tier": "S",
            "weapon_id": 1
        },
        {
            "tierlist_id": 2,
            "tier": "A",
            "weapon_id": 2
        },
        {
            "tierlist_id": 3,
            "tier": "B",
            "weapon_id": 3
        },
        {
            "tierlist_id": 4,
            "tier": "C",
            "weapon_id": 4
        }
    ],
```

**File:** initial_data.json (L54-60)
```json
    "weapon_types": [
        {
            "tipo_id": 1,
            "nombre_tipo": "Espada"
        },
        {
```

 
