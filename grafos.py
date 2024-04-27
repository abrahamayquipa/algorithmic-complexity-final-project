import json
import matplotlib.pyplot as plt
import networkx as nx

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

    # Dibujar el grafo
    nx.draw(G, pos, with_labels=True)

    # Mostrar el grafo
    plt.show()