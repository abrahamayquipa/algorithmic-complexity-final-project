import json
from collections import defaultdict

# Función para cargar el grafo desde el archivo JSON
def cargar_grafo(archivo):
    with open(archivo) as f:
        data = json.load(f)
    grafo = defaultdict(dict)
    aristas = []
    for nodo in data:
        for conexion in nodo["conexiones"]:
            grafo[nodo["idNodo"]][conexion] = nodo["cantidadFinal"]
            grafo[conexion][nodo["idNodo"]] = nodo["cantidadFinal"]
            aristas.append((nodo["cantidadFinal"], nodo["idNodo"], conexion))
    return grafo, aristas

class ConjuntoDisjunto:
    def __init__(self, vertices):
        self.padre = {v: v for v in vertices}
        self.altura = {v: 0 for v in vertices}

    def find(self, e):
        if self.padre[e] != e:
            self.padre[e] = self.find(self.padre[e])
        return self.padre[e]

    def union(self, nodo1, nodo2):
        raiz1 = self.find(nodo1)
        raiz2 = self.find(nodo2)
        if raiz1 != raiz2:
            if self.altura[raiz1] > self.altura[raiz2]:
                self.padre[raiz2] = raiz1
            elif self.altura[raiz1] < self.altura[raiz2]:
                self.padre[raiz1] = raiz2
            else:
                self.padre[raiz2] = raiz1
                self.altura[raiz1] += 1

class MSTKruskal:
    def __init__(self, grafo, aristas):
        self.grafo = grafo
        self.aristas = aristas
        self.mst = []
        self.costoTotal = 0

    def kruskal(self):
        self.aristas.sort()
        conjunto_disjunto = ConjuntoDisjunto(self.grafo.keys())
        for costo, nodo1, nodo2 in self.aristas:
            if conjunto_disjunto.find(nodo1) != conjunto_disjunto.find(nodo2):
                conjunto_disjunto.union(nodo1, nodo2)
                self.mst.append((nodo1, nodo2, costo))
                self.costoTotal += costo

    def get_mst(self):
        return self.mst

    def get_costo_total(self):
        return self.costoTotal

    def reconstruir_mst(self):
        self.mst.sort()
        suma_pesos = sum(peso for _, _, peso in self.mst)
        ruta = " -> ".join(f"{nodo1}-{nodo2}({peso})" for nodo1, nodo2, peso in self.mst)
        return ruta, suma_pesos