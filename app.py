from pymongo import MongoClient
import tkinter as tk
from tkinter import Label, Frame, Scrollbar, Canvas, Listbox
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Conexión a la base de datos
client = MongoClient('mongodb://localhost:27017/')
db = client['DEAD_CELLS']
weapons = db['weapons']
tierlists = db['tierlists']

# Orden de prioridad para las tierlists
tier_priority = {"S": 1, "A": 2, "B": 3, "C": 4, "D": 5}

def mostrar_arma_por_tier(tierlist):
    # Crear ventana para mostrar las armas de la tierlist seleccionada
    top = tk.Toplevel()
    top.title(f"Armas en Tier {tierlist['tier']}")
    top.geometry("1000x700")

    # Canvas con scrollbar
    canvas = Canvas(top)
    scrollbar = Scrollbar(top, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mostrar armas del tier seleccionado
    armas_ids = tierlist["armas"]
    for arma_id in armas_ids:
        arma = weapons.find_one({"_id": arma_id})
        if arma:
            # Crear sub-marco para cada arma
            arma_frame = Frame(scrollable_frame, pady=5, padx=5)
            arma_frame.pack(anchor="w")

            # Descargar y mostrar imagen desde URL (si disponible)
            try:
                if "imagen_url" in arma:
                    response = requests.get(arma["imagen_url"])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data).resize((50, 50))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = Label(arma_frame, image=img_tk)
                    img_label.image = img_tk
                    img_label.pack(side="left", padx=5)
                else:
                    # Si no hay imagen, mostrar texto
                    img_label = Label(arma_frame, text="[Sin imagen]")
                    img_label.pack(side="left", padx=5)
            except Exception:
                # Si la descarga de la imagen falla, mostrar un marcador de error
                img_label = Label(arma_frame, text="[Error al cargar imagen]")
                img_label.pack(side="left", padx=5)

            # Información del arma
            info_label = Label(arma_frame, text=f"{arma['nombre']} ({arma['tipo']})", font=("Arial", 12))
            info_label.pack(side="left")

def mostrar_tierlists():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Selecciona una Tier List de Dead Cells")
    root.geometry("500x400")

    # Mostrar mensaje de bienvenida
    welcome_label = Label(root, text="BIENVENIDO A LA TIERLIST DE DEAD CELLS", font=("Arial", 16, "bold"))
    welcome_label.pack(pady=10)

    # Listbox para mostrar las tierlists disponibles
    tierlist_listbox = Listbox(root, height=10, width=50, selectmode="single")
    tierlist_listbox.pack(pady=10)

    # Obtener todas las tierlists desde MongoDB y aplicamos la prioridad
    tierlist_options = list(tierlists.find())
    tierlist_options.sort(key=lambda x: tier_priority.get(x["tier"], float("inf")))

    # Agregar tierlists al Listbox en orden de prioridad
    for tierlist in tierlist_options:
        tierlist_listbox.insert(tk.END, f"Tier {tierlist['tier']}")

    def on_select_tierlist(event):
        # Obtener la tierlist seleccionada
        selected_index = tierlist_listbox.curselection()
        if selected_index:
            selected_tierlist = tierlist_options[selected_index[0]]
            mostrar_arma_por_tier(selected_tierlist)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tierlist.")

    # Vincular evento de selección
    tierlist_listbox.bind("<<ListboxSelect>>", on_select_tierlist)

    root.mainloop()

if __name__ == '__main__':
    mostrar_tierlists()
