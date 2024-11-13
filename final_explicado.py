from typing import List, Tuple, Optional
import time
from dataclasses import dataclass
import os

# Node representa un nodo de datos en una lista doblemente enlazada
@dataclass
class Node:
    x: int  # Coordenada x en el laberinto
    y: int  # Coordenada y en el laberinto
    next: Optional['Node'] = None  # Puntero al siguiente nodo
    prev: Optional['Node'] = None  # Puntero al nodo anterior

# Clase Stack implementa una pila (estructura LIFO - Last In, First Out)
class Stack:
    def __init__(self):
        self.top = None  # Referencia al nodo en la parte superior de la pila
        self.size = 0    # Tamaño de la pila (número de elementos)

    # Método para agregar un elemento a la pila
    def push(self, x: int, y: int) -> None:
        new_node = Node(x, y)       # Crear un nuevo nodo con las coordenadas (x, y)
        new_node.next = self.top    # Apuntar el nuevo nodo al nodo que actualmente es el tope
        self.top = new_node         # Actualizar el tope de la pila al nuevo nodo
        self.size += 1              # Incrementar el tamaño de la pila

    # Método para remover el elemento en el tope de la pila
    def pop(self) -> Optional[Tuple[int, int]]:
        if not self.top:  # Si la pila está vacía, devolver None
            return None
        coords = (self.top.x, self.top.y)  # Guardar las coordenadas del nodo superior
        self.top = self.top.next           # Mover el tope al siguiente nodo
        self.size -= 1                     # Decrementar el tamaño de la pila
        return coords

# Clase Queue implementa una cola (estructura FIFO - First In, First Out)
class Queue:
    def __init__(self):
        self.front = None  # Referencia al frente de la cola
        self.rear = None   # Referencia al final de la cola
        self.size = 0      # Tamaño de la cola (número de elementos)

    # Método para agregar un elemento a la cola
    def enqueue(self, x: int, y: int) -> None:
        new_node = Node(x, y)  # Crear un nuevo nodo con las coordenadas (x, y)
        if not self.rear:      # Si la cola está vacía, el nuevo nodo es el frente y el final
            self.front = self.rear = new_node
        else:  # Si no está vacía, agregar el nuevo nodo al final
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
        self.size += 1  # Incrementar el tamaño de la cola

    # Método para remover el elemento al frente de la cola
    def dequeue(self) -> Optional[Tuple[int, int]]:
        if not self.front:  # Si la cola está vacía, devolver None
            return None
        coords = (self.front.x, self.front.y)  # Guardar las coordenadas del nodo frontal
        self.front = self.front.next  # Mover el frente al siguiente nodo
        if self.front:  # Si el nuevo frente existe, eliminar la referencia al nodo anterior
            self.front.prev = None
        else:  # Si no, la cola está vacía
            self.rear = None
        self.size -= 1  # Decrementar el tamaño de la cola
        return coords

# Nodo para un árbol (usado en algoritmos que puedan necesitar caminos ramificados)
class TreeNode:
    def __init__(self, x: int, y: int, parent: Optional['TreeNode'] = None):
        self.x = x  # Coordenada x en el laberinto
        self.y = y  # Coordenada y en el laberinto
        self.parent = parent  # Nodo padre (de donde se llegó a este nodo)
        self.children: List['TreeNode'] = []  # Lista de nodos hijos (si se expande el árbol)

# Solución encontrada en el laberinto
@dataclass
class Solution:
    path: List[Tuple[int, int]]  # Lista de coordenadas que conforman el camino
    time_found: float            # Tiempo en que se encontró la solución
    length: int                  # Longitud del camino (número de pasos)

# Clase principal para resolver laberintos
class MazeSolver:
    def __init__(self, size: int, maze_string: str, delay_ms: int):
        self.size = size  # Tamaño del laberinto (n x n)
        # Convertir la cadena de entrada en una matriz (lista de listas)
        self.maze = [list(maze_string[i:i+size]) for i in range(0, len(maze_string), size)]
        self.delay = delay_ms / 1000  # Retraso entre pasos (de milisegundos a segundos)
        self.start = self._find_position('0')  # Buscar la posición inicial (marcada con '0')
        self.end = self._find_position('X')    # Buscar la posición final (marcada con 'X')
        self.solutions: List[Solution] = []    # Lista de soluciones encontradas
        self.current_position = self.start     # Posición actual en el laberinto
        self.start_time = time.time()          # Hora de inicio para medir tiempos

    # Método auxiliar para encontrar la posición de un caracter en la matriz del laberinto
    def _find_position(self, char: str) -> Tuple[int, int]:
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == char:
                    return (i, j)
        return (-1, -1)  # Si no se encuentra, retornar coordenadas inválidas

    # Verificar si un movimiento es válido (dentro de límites y no es una pared)
    def _is_valid_move(self, x: int, y: int, visited: set) -> bool:
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                self.maze[x][y] != '+' and 
                (x, y) not in visited)

    # Imprimir el laberinto en su estado actual
    def _print_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla (Windows o Unix)
        print("+" + "-" * (self.size * 4) + "+")
        for i in range(self.size):
            print("|", end=" ")
            for j in range(self.size):
                cell = self.maze[i][j]
                # Si estamos en la posición actual y no es inicio o fin, marcar con '@'
                if (i, j) == self.current_position and cell not in ['0', 'X']:
                    print("@", end="  ")
                else:
                    print(f"{cell}", end="  ")
            print("|")
        print("+" + "-" * (self.size * 4) + "+")
        time.sleep(self.delay)  # Esperar el tiempo configurado

    # Actualizar la posición actual en el laberinto
    def _move_to(self, x: int, y: int, visited: set):
        old_x, old_y = self.current_position
        
        # Limpiar la posición anterior si no es inicio ni fin
        if self.maze[old_x][old_y] not in ['0', 'X']:
            if (old_x, old_y) in visited:
                self.maze[old_x][old_y] = 'o'  # Marcar como parte del camino
            else:
                self.maze[old_x][old_y] = ' '  # Limpiar

        # Actualizar la posición actual
        self.current_position = (x, y)
        if self.maze[x][y] not in ['0', 'X']:
            self.maze[x][y] = '@'  # Marcar con '@' si no es inicio o fin

        self._print_maze()  # Mostrar el laberinto actualizado

    # Método principal para resolver el laberinto
    def solve(self):
        if not self._verify_maze():
            print("El laberinto no es válido o no tiene solución posible.")
            return
        
        self._find_all_solutions()  # Buscar todas las soluciones posibles
        self._print_final_statistics()  # Imprimir estadísticas finales

    # Verificar que el laberinto tiene posiciones válidas para inicio y fin
    def _verify_maze(self) -> bool:
        return (self.start != (-1, -1) and 
                self.end != (-1, -1) and 
                self.start != self.end)

    # Método para encontrar todas las soluciones posibles usando DFS (Depth-First Search)
    def _find_all_solutions(self):
        visited = set()  # Conjunto de posiciones visitadas
        stack = Stack()  # Utilizar una pila para la exploración DFS
        
        # Agregar la posición inicial a la pila
        stack.push(*self.start)
        visited.add(self.start)
        parent = None

        # Realizar DFS para explorar todas las rutas posibles
        while stack.size > 0:
            current = stack.pop()  # Tomar la posición superior de la pila
            if not current:
                continue

            x, y = current
            self._move_to(x, y, visited)  # Moverse a la posición actual
            if (x, y) == self.end:  # Si se alcanza la posición final
                self._record_solution(parent)
                continue

            # Generar movimientos válidos en todas las direcciones posibles
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self._is_valid_move(nx, ny, visited):
                    stack.push(nx, ny)
                    visited.add((nx, ny))

    # Guardar la solución encontrada
    def _record_solution(self, node: Optional[TreeNode]):
        path = []
        length = 0
        
        # Reconstruir el camino desde el nodo actual hacia atrás
        while node:
            path.append((node.x, node.y))
            node = node.parent
            length += 1
        
        path.reverse()  # Invertir el camino para que vaya del inicio al final
        self.solutions.append(Solution(path, time.time() - self.start_time, length))

    # Imprimir estadísticas finales de todas las soluciones encontradas
    def _print_final_statistics(self):
        if not self.solutions:
            print("No se encontraron soluciones para el laberinto.")
            return
        
        # Mostrar detalles de todas las soluciones
        for idx, solution in enumerate(self.solutions, start=1):
            print(f"Solución {idx}: {solution.length} pasos, encontrada en {solution.time_found:.2f} segundos")
            print(f"Camino: {solution.path}")
