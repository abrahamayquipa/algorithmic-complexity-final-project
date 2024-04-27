import random
import json
import networkx as nx
from grafos import pintar_grafo

ANCHO_PANTALLA = 1920
ALTO_PANTALLA = 1080
NUMERO_CASAS = 1500
MIN_PERSONAS = 1
MAX_PERSONAS = 7
MIN_AGUA_POR_PERSONA = 150
MAX_AGUA_POR_PERSONA = 500
MIN_CONEXIONES = 1
MAX_CONEXIONES = 1500

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

def generar_dataset():
    G = nx.Graph()
    for i in range(1, NUMERO_CASAS + 1):
        nodo = generar_nodo(i)
        G.add_node(nodo["idNodo"], **nodo)
    
    return nx.node_link_data(G)['nodes']

dataset = generar_dataset()

for nodo in dataset:
    del nodo["id"]

with open("dataset.json", "w") as outfile:
    json.dump(dataset, outfile, indent=4)

print("Se ha generado el dataset con éxito.")

dataset_json = "dataset.json"
pintar_grafo(dataset_json)