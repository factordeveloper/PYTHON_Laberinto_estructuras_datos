from typing import List, Tuple, Optional
from dataclasses import dataclass

import time

import os

@dataclass
class Nodo:
    x: int
    y: int
    siguiente: Optional['Nodo'] = None
    anterior: Optional['Nodo'] = None

class Pila:
    def __init__(self):
        self.tope = None
        self.tamaño = 0
    
    def apilar(self, x: int, y: int) -> None:
        nuevo_nodo = Nodo(x, y)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1
    
    def desapilar(self) -> Optional[Tuple[int, int]]:
        if not self.tope:
            return None
        coords = (self.tope.x, self.tope.y)
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return coords

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def encolar(self, x: int, y: int) -> None:
        nuevo_nodo = Nodo(x, y)
        if not self.final:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.final
            self.final = nuevo_nodo
        self.tamaño += 1
    
    def desencolar(self) -> Optional[Tuple[int, int]]:
        if not self.frente:
            return None
        coords = (self.frente.x, self.frente.y)
        self.frente = self.frente.siguiente
        if self.frente:
            self.frente.anterior = None
        else:
            self.final = None
        self.tamaño -= 1
        return coords

class NodoArbol:
    def __init__(self, x: int, y: int, padre: Optional['NodoArbol'] = None):
        self.x = x
        self.y = y
        self.padre = padre
        self.hijos: List['NodoArbol'] = []

@dataclass
class Solucion:
    camino: List[Tuple[int, int]]
    tiempo_encontrado: float
    longitud: int

class SolucionadorLaberinto:
    def __init__(self, tamaño: int, cadena_laberinto: str, retraso_ms: int):
        self.tamaño = tamaño
        self.laberinto = [list(cadena_laberinto[i:i+tamaño]) for i in range(0, len(cadena_laberinto), tamaño)]
        self.retraso = retraso_ms / 1000
        self.inicio = self._encontrar_posicion('0')
        self.fin = self._encontrar_posicion('X')
        self.soluciones: List[Solucion] = []
        self.posicion_actual = self.inicio
        self.tiempo_inicio = time.time()
    
    def _encontrar_posicion(self, char: str) -> Tuple[int, int]:
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                if self.laberinto[i][j] == char:
                    return (i, j)
        return (-1, -1)
    
    def _es_movimiento_valido(self, x: int, y: int, visitados: set) -> bool:
        return (0 <= x < self.tamaño and 
                0 <= y < self.tamaño and 
                self.laberinto[x][y] != '+' and 
                (x, y) not in visitados)
    
    def _imprimir_laberinto(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * (self.tamaño * 4) + "+")
        for i in range(self.tamaño):
            print("|", end=" ")
            for j in range(self.tamaño):
                celda = self.laberinto[i][j]
                if (i, j) == self.posicion_actual and celda not in ['0', 'X']:
                    print("@", end="  ")
                else:
                    print(f"{celda}", end="  ")
            print("|")
        print("+" + "-" * (self.tamaño * 4) + "+")
        time.sleep(self.retraso)
    
    def _mover_a(self, x: int, y: int, visitados: set):
        viejo_x, viejo_y = self.posicion_actual
        
        # Limpiar posición anterior si no es inicio ni fin
        if self.laberinto[viejo_x][viejo_y] not in ['0', 'X']:
            if (viejo_x, viejo_y) in visitados:
                self.laberinto[viejo_x][viejo_y] = 'o'
            else:
                self.laberinto[viejo_x][viejo_y] = ' '
        
        # Actualizar posición actual
        self.posicion_actual = (x, y)
        if self.laberinto[x][y] not in ['0', 'X']:
            self.laberinto[x][y] = '@'
        
        self._imprimir_laberinto()
    
    def resolver(self):
        if not self._verificar_laberinto():
            print("El laberinto no es válido o no tiene solución posible.")
            return
        
        self._encontrar_todas_soluciones()
        self._imprimir_estadisticas_finales()
    
    def _verificar_laberinto(self) -> bool:
        return (self.inicio != (-1, -1) and 
                self.fin != (-1, -1) and 
                self.inicio != self.fin)
    
    def _encontrar_todas_soluciones(self):
        pila = Pila()
        pila.apilar(self.inicio[0], self.inicio[1])
        visitados = {self.inicio}
        camino = [self.inicio]
        
        while pila.tamaño > 0:
            x, y = pila.desapilar() or (0, 0)
            self._mover_a(x, y, visitados)
            
            if (x, y) == self.fin:
                tiempo_solucion = time.time() - self.tiempo_inicio
                self.soluciones.append(Solucion(
                    camino=camino.copy(),
                    tiempo_encontrado=tiempo_solucion,
                    longitud=len(camino)
                ))
                if len(camino) > 1:
                    camino.pop()
                    visitados.remove((x, y))
                continue
            
            # Explorar en las cuatro direcciones
            vecinos = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # derecha, abajo, izquierda, arriba
                nx, ny = x + dx, y + dy
                if self._es_movimiento_valido(nx, ny, visitados):
                    vecinos.append((nx, ny))
            
            # Si no hay movimientos válidos, retroceder
            if not vecinos:
                if len(camino) > 1:
                    camino.pop()
                    if (x, y) not in [self.inicio, self.fin]:
                        visitados.remove((x, y))
                continue
            
            # Agregar vecinos válidos a la pila
            for nx, ny in vecinos:
                pila.apilar(nx, ny)
                visitados.add((nx, ny))
                camino.append((nx, ny))
    
    def _imprimir_estadisticas_finales(self):
        if not self.soluciones:
            print("\nNo se encontraron soluciones.")
            return
        
        mas_corta = min(self.soluciones, key=lambda x: x.longitud)
        mas_larga = max(self.soluciones, key=lambda x: x.longitud)
        tiempo_promedio = sum(sol.tiempo_encontrado for sol in self.soluciones) / len(self.soluciones)
        
        print("\nEstadísticas finales:")
        print(f"Número total de soluciones encontradas: {len(self.soluciones)}")
        
        print("\nSolución más corta:")
        print(f"Longitud: {mas_corta.longitud} pasos")
        print(f"Tiempo: {mas_corta.tiempo_encontrado:.3f} segundos")
        self._imprimir_solucion(mas_corta.camino)
        
        print("\nSolución más larga:")
        print(f"Longitud: {mas_larga.longitud} pasos")
        print(f"Tiempo: {mas_larga.tiempo_encontrado:.3f} segundos")
        self._imprimir_solucion(mas_larga.camino)
        
        print(f"\nTiempo promedio para encontrar solución: {tiempo_promedio:.3f} segundos")
    
    def _imprimir_solucion(self, camino: List[Tuple[int, int]]):
        laberinto_solucion = [[celda for celda in fila] for fila in self.laberinto]
        for x, y in camino:
            if (x, y) not in [self.inicio, self.fin]:
                laberinto_solucion[x][y] = 'o'
        
        print("+" + "-" * (self.tamaño * 4) + "+")
        for fila in laberinto_solucion:
            print("|", end=" ")
            for celda in fila:
                print(f"{celda}", end="  ")
            print("|")
        print("+" + "-" * (self.tamaño * 4) + "+")

def main():
    # Solicitar datos al usuario
    tamaño = int(input("Ingrese el tamaño del laberinto (n x n): "))
    print("\nUse los siguientes caracteres:")
    print("0: Posición inicial")
    print("X: Posición final")
    print("+: Paredes (No transitables)")
    print("  (espacio): Celdas transitables")
    cadena_laberinto = input(f"\nIngrese el laberinto como una cadena de {tamaño*tamaño} caracteres: ")
    retraso = int(input("Ingrese el retraso entre pasos (milisegundos): "))
    
    # Validar entrada
    if len(cadena_laberinto) != tamaño * tamaño:
        print(f"Error: La cadena debe tener exactamente {tamaño*tamaño} caracteres")
        return
    
    # Resolver el laberinto
    solucionador = SolucionadorLaberinto(tamaño, cadena_laberinto, retraso)
    solucionador.resolver()

if __name__ == "__main__":
    main()