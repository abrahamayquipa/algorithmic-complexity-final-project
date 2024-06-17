import json
from collections import defaultdict, deque
import time
import tkinter as interface
from tkinter import ttk, messagebox
from ventana import centrarVentana
from prim import cargar_grafo as cargar_grafo_prim, prim, reconstruir_ruta
from kruskal import cargar_grafo as cargar_grafo_kruskal, kruskal, reconstruir_mst
from fulkerson import cargar_grafo as cargar_grafo_ford_fulkerson, ford_fulkerson
import networkx as nx
import matplotlib.pyplot as plt

dataset_json = "dataset.json"
ruta_global = None
algoritmo_global = None
aristas_global = None
informacion_casas = {}
nombre_a_id = {}
id_a_nombre = {}

def cargar_nodos(dataset_json):
    global informacion_casas, nombre_a_id, id_a_nombre
    with open(dataset_json, "r") as archivo:
        lista_casas = json.load(archivo)
    nodos = [nodo["ubicacion"]["nombre"] for nodo in lista_casas]
    informacion_casas = {nodo["ubicacion"]["nombre"]: nodo for nodo in lista_casas}
    nombre_a_id = {nodo["ubicacion"]["nombre"]: nodo["idNodo"] for nodo in lista_casas}
    id_a_nombre = {nodo["idNodo"]: nodo["ubicacion"]["nombre"] for nodo in lista_casas}
    return nodos

def generar_grafo(ruta):
    arreglo = ruta.split('->')

    # Creamos un grafo dirigido
    G = nx.DiGraph()

    # Agregamos nodos al grafo
    for i, valor in enumerate(arreglo):
        G.add_node(i, label=str(valor))

    # Agregamos aristas entre nodos consecutivos
    for i in range(len(arreglo) - 1):
        G.add_edge(i, i + 1)

    # Dibujamos el grafo
    pos = nx.spring_layout(G)  # Layout para posicionar los nodos
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
            node_color='lightblue', node_size=2000, font_size=10, font_color='black', edge_color='black', width=2.0)

    # Mostramos el grafo
    plt.title('Grafo con Arreglo')
    plt.show()

def obtener_aristas_de_ruta(ruta, grafo):
    aristas = []
    for i in range(len(ruta) - 1):
        u = ruta[i]
        v = ruta[i + 1]
        for vecino, peso in grafo[u]:
            if vecino == v:
                aristas.append((u, v, peso))
                break
    return aristas

def calcular_ruta_mas_corta(algoritmo, valor1, valor2):
    global ruta_global, algoritmo_global, aristas_global

    if not valor1 or not valor2:
        messagebox.showwarning("Advertencia", "Seleccione la conexión de origen y la conexión de llegada.")
        return

    id1 = nombre_a_id[valor1]
    id2 = nombre_a_id[valor2]

    if algoritmo.get() == "Prim":
        grafo = cargar_grafo_prim(dataset_json)
        inicio = time.perf_counter()
        padre, costo, aristas = prim(grafo, id1)
        ruta, suma_pesos = reconstruir_ruta(padre, id1, id2, grafo)
        # Medicion de tiempo
        fin = time.perf_counter()
        tiempo_prim = (fin - inicio) * 1000
        aristas_global = obtener_aristas_de_ruta(ruta.split('->'), grafo)
        tiempo_ejecucion = f"Tiempo de ejecución de Prim: {tiempo_prim:.2f} ms"
    elif algoritmo.get() == "Kruskal":
        grafo, aristas = cargar_grafo_kruskal(dataset_json)
        inicio = time.perf_counter()
        mst = kruskal(grafo, aristas)
        ruta, suma_pesos = reconstruir_mst(mst)
        # Medicion de tiempo
        fin = time.perf_counter()
        tiempo_kruskal = (fin - inicio) * 1000
        aristas_global = obtener_aristas_de_ruta(ruta.split('->'), grafo)
        tiempo_ejecucion = f"Tiempo de ejecución de Kruskal: {tiempo_kruskal:.2f} ms"
    elif algoritmo.get() == "Ford-Fulkerson":
        grafo = cargar_grafo_ford_fulkerson(dataset_json)
        # Medicion de tiempo
        inicio = time.perf_counter()
        suma_pesos = ford_fulkerson(grafo, id1, id2)
        fin = time.perf_counter()
        tiempo_ford_fulkerson = (fin - inicio) * 1000
        ruta = [id1, id2]
        aristas_global = [(id1, id2, suma_pesos)]
        tiempo_ejecucion = f"Tiempo de ejecución de Ford-Fulkerson: {tiempo_ford_fulkerson:.2f} ms"

    ruta_global = ruta
    algoritmo_global = algoritmo

    ventanaMatriz = interface.Toplevel(aplicacion)
    ventanaMatriz.configure(bg='lightblue')
    ventanaMatriz.title(f"Calculadora de la ruta más corta entre dos casas - {algoritmo.get()}")

    centrarVentana(ventanaMatriz)

    # Mostrar información de las casas seleccionadas
    info_origen = informacion_casas[valor1]
    info_destino = informacion_casas[valor2]

    interface.Label(ventanaMatriz, text=f"Casa {valor1}:", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Personas: {info_origen['personasQueVivenDentroDeLaCasa']}", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Agua por persona: {info_origen['cantidadRegularDeAguaEstimadaXpersona']} litros", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Total de agua: {info_origen['cantidadFinal']} litros", bg='lightblue').pack(pady=5)

    interface.Label(ventanaMatriz, text=f"Casa {valor2}:", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Personas: {info_destino['personasQueVivenDentroDeLaCasa']}", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Agua por persona: {info_destino['cantidadRegularDeAguaEstimadaXpersona']} litros", bg='lightblue').pack(pady=5)
    interface.Label(ventanaMatriz, text=f"  Total de agua: {info_destino['cantidadFinal']} litros", bg='lightblue').pack(pady=5)

    # Mostrar la ruta y el peso total
    interface.Label(ventanaMatriz, text=f"La ruta final entre la casa {valor1} y la casa {valor2} es: {ruta}", bg='lightblue').pack(pady=10)
    interface.Label(ventanaMatriz, text=f"La distancia más óptima para enviar agua sin perdida de presión es: {suma_pesos} metros", bg='lightblue').pack(pady=10)

    # Mostrar el tiempo de ejecución
    interface.Label(ventanaMatriz, text=tiempo_ejecucion, bg='lightblue').pack(pady=10)

    frame_grafico = interface.Frame(ventanaMatriz, bg='lightblue')
    frame_grafico.pack(fill=interface.BOTH, expand=True)

    interface.Button(ventanaMatriz, text="Generar Gráfico", command=lambda: generar_grafo(ruta), bg='blue', fg='white').pack(pady=10)
    centrarVentana(ventanaMatriz)

aplicacion = interface.Tk()
aplicacion.configure(bg='lightblue')
aplicacion.title("Dashboard")

interface.Label(aplicacion, text="Seleccione la primera casa:", bg='lightblue').pack(pady=10)
valorCasa1 = interface.StringVar(aplicacion)
opciones_nodos = cargar_nodos(dataset_json)
dropdown1 = ttk.Combobox(aplicacion, textvariable=valorCasa1, values=opciones_nodos)
dropdown1.pack(pady=10, padx=200)

interface.Label(aplicacion, text="Seleccione la segunda casa:", bg='lightblue').pack(pady=10)
valorCasa2 = interface.StringVar(aplicacion)
dropdown2 = ttk.Combobox(aplicacion, textvariable=valorCasa2, values=opciones_nodos)
dropdown2.pack(pady=10, padx=200)

interface.Label(aplicacion, text="Seleccione el algoritmo:", bg='lightblue').pack(pady=10)
algoritmo_var = interface.StringVar(value="Prim")
interface.Radiobutton(aplicacion, text="Prim", variable=algoritmo_var, value="Prim", bg='lightblue').pack(pady=5)
interface.Radiobutton(aplicacion, text="Kruskal", variable=algoritmo_var, value="Kruskal", bg='lightblue').pack(pady=5)
interface.Radiobutton(aplicacion, text="Ford-Fulkerson", variable=algoritmo_var, value="Ford-Fulkerson", bg='lightblue').pack(pady=5)

interface.Button(aplicacion, text="Calcular", command=lambda: calcular_ruta_mas_corta(algoritmo_var, valorCasa1.get(), valorCasa2.get()), bg='blue', fg='white').pack(pady=20)

centrarVentana(aplicacion)
aplicacion.mainloop()