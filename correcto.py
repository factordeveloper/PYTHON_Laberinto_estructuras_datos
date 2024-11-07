from collections import deque
from typing import List, Tuple
import time

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

    def _crear_matriz_laberinto(self, cadena_laberinto: str) -> List[List[str]]:
        return [list(cadena_laberinto[i:i+self.tamanio]) for i in range(0, len(cadena_laberinto), self.tamanio)]
    
    def _encontrar_posicion(self, caracter: str) -> Tuple[int, int]:
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self.laberinto[i][j] == caracter:
                    return (i, j)
        return (-1, -1)
    
    def _es_movimiento_valido(self, x: int, y: int, visitados: set) -> bool:
        return (0 <= x < self.tamanio and 
                0 <= y < self.tamanio and 
                self.laberinto[x][y] != '+' and 
                (x, y) not in visitados)
    
    def _imprimir_laberinto(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * (self.tamanio * 3) + "+")
        for fila in self.laberinto:
            print("|", end=" ")
            for celda in fila:
                print(f"{celda} ", end=" ")
            print("|")
        print("+" + "-" * (self.tamanio * 3) + "+")
        time.sleep(self.retraso)
    
    def _es_alcanzable(self) -> bool:
        if self.inicio == (-1, -1) or self.fin == (-1, -1):
            return False

        visitados = set()
        cola = deque([self.inicio])

        while cola:
            x, y = cola.popleft()
            if (x, y) == self.fin:
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._es_movimiento_valido(nx, ny, visitados):
                    visitados.add((nx, ny))
                    cola.append((nx, ny))

        return False

    def resolver(self):
        if not self._es_alcanzable():
            print("No se encontró solución: el destino no es alcanzable desde el inicio.")
            return

        tiempo_inicio = time.time()
        visitados = set()
        cola = deque([(self.inicio, [self.inicio])])

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == self.fin:
                solucion = Solucion(camino, time.time() - tiempo_inicio)
                self.soluciones.append(solucion)
                self._mostrar_recorrido(solucion)
            else:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if self._es_movimiento_valido(nx, ny, visitados):
                        visitados.add((nx, ny))
                        nuevo_camino = camino + [(nx, ny)]
                        cola.append(((nx, ny), nuevo_camino))
        
        if not self.soluciones:
            print("No se encontró solución")
        else:
            self._imprimir_estadisticas()
    
    def _mostrar_recorrido(self, solucion: Solucion):
        for x, y in solucion.camino:
            if (x, y) != self.inicio and (x, y) != self.fin:
                self.laberinto[x][y] = '🐢'
                self._imprimir_laberinto()
                self.laberinto[x][y] = 'o'
    
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
    cadena_laberinto = input(f"Ingrese el laberinto como una cadena de {tamanio*tamanio} caracteres: ")
    retraso = int(input("Ingrese el retraso entre pasos (milisegundos): "))
    
    if len(cadena_laberinto) != tamanio * tamanio:
        print(f"Error: La cadena debe tener exactamente {tamanio*tamanio} caracteres")
        return
    
    laberinto = Laberinto(tamanio, cadena_laberinto, retraso)
    laberinto.resolver()

if __name__ == "__main__":
    main()
