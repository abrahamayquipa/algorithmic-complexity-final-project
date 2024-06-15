import json
from collections import defaultdict, deque

# Función para cargar el grafo desde el archivo JSON
def cargar_grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(dict)
    for nodo in data:
        for conexion in nodo["conexiones"]:
            grafo[nodo["idNodo"]][conexion] = nodo["cantidadFinal"]
    return grafo

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
    camino_residual = defaultdict(lambda: defaultdict(int))
    
    for u in grafo:
        for v in grafo[u]:
            camino_residual[u][v] = grafo[u][v]
    
    flujo_maximo = 0
    padre = {}
    
    while bfs(camino_residual, fuente, sumidero, padre):
        flujo_path = float('Inf')
        s = sumidero
        
        while s != fuente:
            flujo_path = min(flujo_path, camino_residual[padre[s]][s])
            s = padre[s]
        
        v = sumidero
        while v != fuente:
            u = padre[v]
            camino_residual[u][v] -= flujo_path
            camino_residual[v][u] += flujo_path
            v = padre[v]
        
        flujo_maximo += flujo_path
    
    return flujo_maximo
