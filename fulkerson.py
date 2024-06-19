import json
from collections import defaultdict, deque

# Función para cargar el grafo desde el archivo JSON
def cargar_grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(list)
    for nodo in data:
        for conexion in nodo["conexiones"]:
            grafo[nodo["idNodo"]].append((conexion, nodo["cantidadFinal"]))
    return grafo

def crea_grafo_residual(grafo):
    grafo_residual = defaultdict(lambda: defaultdict(int))
    for u in grafo:
        for v, capacidad in grafo[u]:
            grafo_residual[u][v] = capacidad
            grafo_residual[v][u] = 0
    return grafo_residual

def bfs(camino_residual, fuente, sumidero, padre):
    visitados = set()
    cola = deque([fuente])
    visitados.add(fuente)
    
    while cola:
        nodo = cola.popleft()
        
        for vecino, capacidad in camino_residual[nodo].items():
            if vecino not in visitados and capacidad > 0:
                cola.append(vecino)
                visitados.add(vecino)
                padre[vecino] = nodo
                if vecino == sumidero:
                    return True
    return False

def ford_fulkerson(grafo, fuente, sumidero):
    grafo_residual = crea_grafo_residual(grafo)
    flujo_maximo = 0
    padre = {}
    rutas = []
    
    while bfs(grafo_residual, fuente, sumidero, padre):
        flujo_path = float('Inf')
        s = sumidero
        
        while s != fuente:
            flujo_path = min(flujo_path, grafo_residual[padre[s]][s])
            s = padre[s]
        
        v = sumidero
        while v != fuente:
            u = padre[v]
            grafo_residual[u][v] -= flujo_path
            grafo_residual[v][u] += flujo_path
            v = padre[v]
        
        flujo_maximo += flujo_path
        ruta = []
        nodo = sumidero
        while nodo != fuente:
            ruta.append(nodo)
            nodo = padre[nodo]
        ruta.append(fuente)
        ruta.reverse()
        rutas.append(ruta)
    
    return flujo_maximo, rutas

