import pymongo
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
import textwrap

# Conexión a MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['DEAD_CELLS']
weapons = db['weapons']
tierlists = db['tierlists']

# Función para obtener armas y sus tiers
def obtener_armas_por_tiers():
    armas_por_tier = {'S': [], 'A': [], 'B': [], 'C': [], 'D': []}

    for tierlist in tierlists.find():
        tier = tierlist.get('tier', 'Desconocido')
        armas_ids = tierlist.get('armas', [])
        for arma_id in armas_ids:
            arma = weapons.find_one({"_id": arma_id})
            if arma:
                armas_por_tier[tier].append({
                    "nombre": arma['nombre'],
                    "imagen_url": arma.get('imagen_url', '')
                })

    return armas_por_tier

# Función para descargar la imagen desde una URL
def obtener_imagen(imagen_url):
    try:
        response = requests.get(imagen_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize((64, 64))  # Redimensionamos a un tamaño uniforme
            return img
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
    return None

# Función para convertir colores RGB a valores normalizados de matplotlib
def rgb_color(rgb_tuple):
    return tuple(c / 255.0 for c in rgb_tuple)

# Función para mostrar las armas en un formato similar al de la imagen
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
