import json
from collections import defaultdict

# Función para cargar el grafo desde el archivo JSON
def cargar_grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(list)
    aristas = []
    for nodo in data:
        for conexion in nodo["conexiones"]:
            grafo[nodo["idNodo"]].append((conexion, nodo["cantidadFinal"]))
            grafo[conexion].append((nodo["idNodo"], nodo["cantidadFinal"]))
            aristas.append((nodo["cantidadFinal"], nodo["idNodo"], conexion))
    return grafo, aristas

def encontrar(padre, nodo):
    if padre[nodo] == nodo:
        return nodo
    return encontrar(padre, padre[nodo])

def unir(padre, rango, nodo1, nodo2):
    raiz1 = encontrar(padre, nodo1)
    raiz2 = encontrar(padre, nodo2)
    
    if rango[raiz1] < rango[raiz2]:
        padre[raiz1] = raiz2
    elif rango[raiz1] > rango[raiz2]:
        padre[raiz2] = raiz1
    else:
        padre[raiz2] = raiz1
        rango[raiz1] += 1

def kruskal(grafo, aristas):
    aristas.sort()  
    padre = {}
    rango = {}
    
    for nodo in grafo:
        padre[nodo] = nodo
        rango[nodo] = 0
    
    mst = []
    for peso, nodo1, nodo2 in aristas:
        if encontrar(padre, nodo1) != encontrar(padre, nodo2):
            unir(padre, rango, nodo1, nodo2)
            mst.append((nodo1, nodo2, peso))
    
    return mst

def reconstruir_mst(mst):
    mst.sort()
    suma_pesos = sum(peso for _, _, peso in mst)
    ruta = " -> ".join(f"{nodo1}-{nodo2}({peso})" for nodo1, nodo2, peso in mst)
    return ruta, suma_pesos
