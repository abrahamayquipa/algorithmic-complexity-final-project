import json
import networkx as nx
from grafos import pintar_grafo
from grafos import generar_nodo

NUMERO_CASAS = 1500

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

# dataset_json = "dataset.json"
# pintar_grafo(dataset_json)