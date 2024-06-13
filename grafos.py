import json
import random
import matplotlib.pyplot as plt
import networkx as nx

ANCHO_PANTALLA = 1920
ALTO_PANTALLA = 1080
NUMERO_CASAS = 1500
MIN_PERSONAS = 1
MAX_PERSONAS = 7
MIN_AGUA_POR_PERSONA = 150
MAX_AGUA_POR_PERSONA = 500
MIN_CONEXIONES = 1
MAX_CONEXIONES = 1500

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

    # Ajustar las dimensiones a pantalla completa
    fig = plt.figure()
    fig.set_size_inches(16, 9)

    # Dibujar el grafo
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=12)

    # Ajustar el diseño para que se vea bien
    plt.tight_layout()

    # Mostrar el grafo
    plt.show()

def generar_aleatorio(minimo, maximo):
    return random.randint(minimo, maximo)

def generar_nodo(id_nodo):
    ubicacion = {
        "x": generar_aleatorio(0, ANCHO_PANTALLA),
        "y": generar_aleatorio(0, ALTO_PANTALLA)
    }
    personas_que_viven = generar_aleatorio(MIN_PERSONAS, MAX_PERSONAS)
    conexiones = [generar_aleatorio(1, NUMERO_CASAS), generar_aleatorio(1, NUMERO_CASAS)]
    cantidad_regular_estimada_x_persona = generar_aleatorio(MIN_AGUA_POR_PERSONA, MAX_AGUA_POR_PERSONA)
    cantidad_final = personas_que_viven * cantidad_regular_estimada_x_persona

    nodo = {
        "idNodo": id_nodo,
        "ubicacion": ubicacion,
        "personasQueVivenDentroDeLaCasa": personas_que_viven,
        "conexiones": conexiones,
        "cantidadRegularDeAguaEstimadaXpersona": cantidad_regular_estimada_x_persona,
        "cantidadFinal": cantidad_final
    }
    return nodo