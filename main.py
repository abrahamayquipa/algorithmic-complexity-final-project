import json
import networkx as nx
import tkinter as interface
import matplotlib.pyplot as plt
from ventana import centrarVentana
from prim import cargar_grafo, prim, reconstruir_ruta

dataset_json = "algorithmic-complexity-final-project/dataset.json"

def pintar_grafo(dataset_json):
    # Cargar el dataset desde el archivo JSON
    with open(dataset_json, "r") as archivo:
        lista_casas = json.load(archivo)

    # Crear un grafo de NetworkX
    G = nx.Graph()

    # Agregar nodos al grafo
    for nodo in lista_casas:
        G.add_node(nodo["idNodo"], pos=(nodo["ubicacion"]["x"], nodo["ubicacion"]["y"]))

    # Agregar conexiones al grafo
    for nodo in lista_casas:
        for conexion in nodo["conexiones"]:
            G.add_edge(nodo["idNodo"], conexion)

    # Obtener posiciones de los nodos
    pos = nx.get_node_attributes(G, "pos")

    # Ajustar el tamaño de la figura para que ocupe toda la pantalla
    fig = plt.figure()
    fig.set_size_inches(16, 9)  # Cambia estas dimensiones según la resolución de tu pantalla

    # Dibujar el grafo
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=12)

    # Ajustar el diseño para que se vea bien
    plt.tight_layout()

    # Mostrar el grafo
    plt.show()

def calcularRutaMasCorta(valor1, valor2):
    valor1 = int(valor1.get())
    valor2 = int(valor2.get())

    # Cargar el grafo y calcular la ruta más corta
    grafo = cargar_grafo(dataset_json)
    padre, costo, aristas = prim(grafo, valor1)
    ruta, suma_pesos = reconstruir_ruta(padre, valor1, valor2, grafo)

    # Crear ventana secundaria para mostrar el resultado
    ventanaMatriz = interface.Toplevel(aplicacion)
    ventanaMatriz.title("Calculadora de la ruta más corta entre dos casas")

    centrarVentana(ventanaMatriz)

    # Mostrar la ruta y el peso total
    interface.Label(ventanaMatriz, text=f"La ruta final entre la casa {valor1} y la casa {valor2} es: {ruta}").pack(pady=10)
    interface.Label(ventanaMatriz, text=f"La suma de los pesos de las aristas que conforman la ruta final es: {suma_pesos}").pack(pady=10)

# Pintar el grafo al inicio
pintar_grafo(dataset_json)

# Configuración de la interfaz gráfica principal
aplicacion = interface.Tk()
aplicacion.title("Dashboard")

interface.Label(aplicacion, text="Ingrese el número de la primera casa:").pack(pady=10)
valorCasa1 = interface.Entry(aplicacion)
valorCasa1.pack(pady=10, padx=200)

interface.Label(aplicacion, text="Ingrese el número de la segunda casa:").pack(pady=10)
valorCasa2 = interface.Entry(aplicacion)
valorCasa2.pack(pady=10, padx=200)

interface.Button(aplicacion, text="Generar la ruta más corta", command=lambda: calcularRutaMasCorta(valorCasa1, valorCasa2)).pack(pady=10)

centrarVentana(aplicacion)
aplicacion.mainloop()