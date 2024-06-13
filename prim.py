import json
from collections import defaultdict

# Función para cargar el grafo desde el archivo JSON
def cargar_grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(list)
    for nodo in data:
        for conexion in nodo["conexiones"]:
            grafo[nodo["idNodo"]].append((conexion, nodo["cantidadFinal"]))
            grafo[conexion].append((nodo["idNodo"], nodo["cantidadFinal"]))
    return grafo

# Función para implementar el algoritmo de Prim
def prim(grafo, inicio):
    visitados = set()
    aristas = []
    padre = {}
    costo = {}
    for nodo in grafo:
        costo[nodo] = float('inf')
    costo[inicio] = 0
    
    while len(visitados) != len(grafo):
        nodo_min = None
        for nodo in grafo:
            if nodo not in visitados and (nodo_min is None or costo[nodo] < costo[nodo_min]):
                nodo_min = nodo
        if nodo_min is None:
            break
        visitados.add(nodo_min)
        for vecino, peso in grafo[nodo_min]:
            if vecino not in visitados and peso < costo[vecino]:
                padre[vecino] = nodo_min
                costo[vecino] = peso
                aristas.append((nodo_min, vecino, peso))
    return padre, costo, aristas

# Función para reconstruir la ruta más corta y calcular la suma de pesos
def reconstruir_ruta(padre, inicio, fin, grafo):
    ruta = []
    nodo = fin
    suma_pesos = 0
    while nodo != inicio:
        ruta.append(nodo)
        nodo_padre = padre[nodo]
        for vecino, peso in grafo[nodo_padre]:
            if vecino == nodo:
                suma_pesos += peso
                break
        nodo = nodo_padre
    ruta.append(inicio)
    ruta.reverse()
    return "->".join(str(nodo) for nodo in ruta), suma_pesos