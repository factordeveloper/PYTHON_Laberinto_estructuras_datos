import time
from collections import deque
from typing import List, Tuple, Set
import os

class Solucion:
    def __init__(self, camino: List[Tuple[int, int]], tiempo_encontrado: float):
        self.camino = camino
        self.tiempo_encontrado = tiempo_encontrado
        self.longitud = len(camino)

class Laberinto:
    def __init__(self, tamanio: int, cadena_laberinto: str, retraso_ms: int):
        self.tamanio = tamanio
        self.laberinto = self._crear_matriz_laberinto(cadena_laberinto)
        self.retraso = retraso_ms / 1000
        self.inicio = self._encontrar_posicion('0')
        self.fin = self._encontrar_posicion('X')
        self.soluciones: List[Solucion] = []
        self.tiempo_inicio = 0

    def _crear_matriz_laberinto(self, cadena_laberinto: str) -> List[List[str]]:
        return [list(cadena_laberinto[i:i + self.tamanio]) for i in range(0, len(cadena_laberinto), self.tamanio)]
    
    def _encontrar_posicion(self, caracter: str) -> Tuple[int, int]:
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self.laberinto[i][j] == caracter:
                    return (i, j)
        return (-1, -1)
    
    def _es_movimiento_valido(self, x: int, y: int, visitados: Set[Tuple[int, int]]) -> bool:
        return (0 <= x < self.tamanio and 
                0 <= y < self.tamanio and 
                self.laberinto[x][y] != '+' and 
                (x, y) not in visitados)
    
    def _imprimir_laberinto(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * (self.tamanio * 3) + "+")
        for fila in self.laberinto:
            print("|", end=" ")
            for celda in fila:
                print(f"{celda} ", end=" ")
            print("|")
        print("+" + "-" * (self.tamanio * 3) + "+")
        time.sleep(self.retraso)

    def resolver(self):
        self.tiempo_inicio = time.time()
        pila = [(self.inicio, [self.inicio], set([self.inicio]))]

        while pila:
            (x, y), camino_actual, visitados = pila.pop()
            
            if (x, y) == self.fin:
                self.soluciones.append(Solucion(camino_actual, time.time() - self.tiempo_inicio))
                self._imprimir_laberinto()
                continue
            
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if self._es_movimiento_valido(nx, ny, visitados):
                    nuevo_camino = camino_actual + [(nx, ny)]
                    nuevo_visitados = visitados | {(nx, ny)}
                    pila.append(((nx, ny), nuevo_camino, nuevo_visitados))

                    # Marcar el camino en el laberinto
                    if (nx, ny) != self.fin:
                        self.laberinto[nx][ny] = '🐢'
                    self._imprimir_laberinto()
                    if (nx, ny) != self.fin:
                        self.laberinto[nx][ny] = 'o'

        if not self.soluciones:
            print("No se encontró solución")
        else:
            self._imprimir_estadisticas()

    def _imprimir_estadisticas(self):
        mas_corta = min(self.soluciones, key=lambda x: x.longitud)
        mas_larga = max(self.soluciones, key=lambda x: x.longitud)
        tiempo_promedio = sum(sol.tiempo_encontrado for sol in self.soluciones) / len(self.soluciones)
        
        print("\nEstadísticas:")
        print(f"Total de soluciones encontradas: {len(self.soluciones)}")
        print(f"\nSolución más corta (longitud {mas_corta.longitud}):")
        self._imprimir_solucion(mas_corta.camino)
        print(f"Tiempo para encontrar: {mas_corta.tiempo_encontrado:.2f} segundos")
        
        print(f"\nSolución más larga (longitud {mas_larga.longitud}):")
        self._imprimir_solucion(mas_larga.camino)
        print(f"Tiempo para encontrar: {mas_larga.tiempo_encontrado:.2f} segundos")
        
        print(f"\nTiempo promedio para encontrar una solución: {tiempo_promedio:.2f} segundos")

    def _imprimir_solucion(self, camino: List[Tuple[int, int]]):
        laberinto_solucion = [[celda for celda in fila] for fila in self.laberinto]
        
        for x, y in camino:
            if (x, y) != self.inicio and (x, y) != self.fin:
                laberinto_solucion[x][y] = 'o'
        
        print("+" + "-" * (self.tamanio * 3) + "+")
        for fila in laberinto_solucion:
            print("|", end=" ")
            for celda in fila:
                print(f"{celda} ", end=" ")
            print("|")
        print("+" + "-" * (self.tamanio * 3) + "+")

def main():
    tamanio = int(input("Ingrese el tamaño del laberinto (n x n): "))
    cadena_laberinto = input(f"Ingrese el laberinto como una cadena de {tamanio * tamanio} caracteres: ")
    retraso = int(input("Ingrese el retraso entre pasos (milisegundos): "))
    
    if len(cadena_laberinto) != tamanio * tamanio:
        print(f"Error: La cadena debe tener exactamente {tamanio * tamanio} caracteres")
        return
    
    laberinto = Laberinto(tamanio, cadena_laberinto, retraso)
    laberinto.resolver()

if __name__ == "__main__":
    main()
