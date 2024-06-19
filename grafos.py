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
MAX_CONEXIONES = 3

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

def cargar_calles():
    with open("streets.json", "r") as archivo:
        return json.load(archivo)

def generar_nombre_unico(id_nodo, calles):
    calle = random.choice(calles)
    return f"{calle} {id_nodo}"

def generar_nodo(id_nodo, calles):
    ubicacion = {
        "nombre": generar_nombre_unico(id_nodo, calles),
        "x": generar_aleatorio(0, ANCHO_PANTALLA),
        "y": generar_aleatorio(0, ALTO_PANTALLA)
    }
    personas_que_viven = generar_aleatorio(MIN_PERSONAS, MAX_PERSONAS)
    cantidad_regular_estimada_x_persona = generar_aleatorio(MIN_AGUA_POR_PERSONA, MAX_AGUA_POR_PERSONA)
    cantidad_final = personas_que_viven * cantidad_regular_estimada_x_persona

    nodo = {
        "idNodo": id_nodo,
        "ubicacion": ubicacion,
        "personasQueVivenDentroDeLaCasa": personas_que_viven,
        "conexiones": [],
        "cantidadRegularDeAguaEstimadaXpersona": cantidad_regular_estimada_x_persona,
        "cantidadFinal": cantidad_final
    }
    return nodo

def generar_grafo():
    calles = cargar_calles()
    nodos = [generar_nodo(i, calles) for i in range(1, NUMERO_CASAS + 1)]

    # Crear un grafo de NetworkX para asegurar que no haya muchos ciclos
    G = nx.Graph()

    # Agregar nodos al grafo
    for nodo in nodos:
        G.add_node(nodo["idNodo"], pos=(nodo["ubicacion"]["x"], nodo["ubicacion"]["y"]))

    # Agregar conexiones al grafo de manera controlada
    for nodo in nodos:
        conexiones = set()
        while len(conexiones) < generar_aleatorio(MIN_CONEXIONES, MAX_CONEXIONES):
            posible_conexion = generar_aleatorio(1, NUMERO_CASAS)
            if posible_conexion != nodo["idNodo"]:
                conexiones.add(posible_conexion)
        nodo["conexiones"] = list(conexiones)
        for conexion in conexiones:
            G.add_edge(nodo["idNodo"], conexion)

    # Asegurar que el grafo no tenga demasiados ciclos
    if not nx.is_connected(G):
        print("El grafo no es conexo. Conectando componentes...")
        for component in list(nx.connected_components(G))[1:]:
            nodo_random = random.choice(list(component))
            conexion_random = random.choice(list(nx.connected_components(G)[0]))
            G.add_edge(nodo_random, conexion_random)

    # Exportar el dataset a un archivo JSON
    with open("dataset.json", "w") as archivo:
        json.dump(nodos, archivo, indent=4)

    return "dataset.json"

dataset_json = generar_grafo()