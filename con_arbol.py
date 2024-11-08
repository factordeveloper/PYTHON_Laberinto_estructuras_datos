from typing import List, Tuple, Optional
import time
from dataclasses import dataclass
import os

@dataclass
class Node:
    x: int
    y: int
    next: Optional['Node'] = None
    prev: Optional['Node'] = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
    
    def push(self, x: int, y: int) -> None:
        new_node = Node(x, y)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self) -> Optional[Tuple[int, int]]:
        if not self.top:
            return None
        coords = (self.top.x, self.top.y)
        self.top = self.top.next
        self.size -= 1
        return coords

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, x: int, y: int) -> None:
        new_node = Node(x, y)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
        self.size += 1
    
    def dequeue(self) -> Optional[Tuple[int, int]]:
        if not self.front:
            return None
        coords = (self.front.x, self.front.y)
        self.front = self.front.next
        if self.front:
            self.front.prev = None
        else:
            self.rear = None
        self.size -= 1
        return coords

class TreeNode:
    def __init__(self, x: int, y: int, parent: Optional['TreeNode'] = None):
        self.x = x
        self.y = y
        self.parent = parent
        self.children: List['TreeNode'] = []

@dataclass
class Solution:
    path: List[Tuple[int, int]]
    time_found: float
    length: int

class MazeSolver:
    def __init__(self, size: int, maze_string: str, delay_ms: int):
        self.size = size
        self.maze = [list(maze_string[i:i+size]) for i in range(0, len(maze_string), size)]
        self.delay = delay_ms / 1000
        self.start = self._find_position('0')
        self.end = self._find_position('X')
        self.solutions: List[Solution] = []
        self.current_turtle = self.start
    
    def _find_position(self, char: str) -> Tuple[int, int]:
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == char:
                    return (i, j)
        return (-1, -1)
    
    def _is_valid_move(self, x: int, y: int, visited: set) -> bool:
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                self.maze[x][y] != '+' and 
                (x, y) not in visited)
    
    def _print_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * (self.size * 3) + "+")
        for row in self.maze:
            print("|", end=" ")
            for cell in row:
                print(f"{cell} ", end=" ")
            print("|")
        print("+" + "-" * (self.size * 3) + "+")
        time.sleep(self.delay)
    
    def _animate_turtle_movement(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        if from_pos != self.start:
            self.maze[from_pos[0]][from_pos[1]] = 'o'
        
        # Animación del movimiento
        path = self._get_path_between(from_pos, to_pos)
        for pos in path:
            if pos != self.start and pos != self.end:
                self.maze[pos[0]][pos[1]] = '🐢'
                self._print_maze()
                self.maze[pos[0]][pos[1]] = 'o'
    
    def _get_path_between(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        x1, y1 = start
        x2, y2 = end
        
        # Movimiento horizontal
        while y1 != y2:
            y1 += 1 if y2 > y1 else -1
            if self._is_valid_move(x1, y1, set()):
                path.append((x1, y1))
            else:
                break
        
        # Movimiento vertical
        while x1 != x2:
            x1 += 1 if x2 > x1 else -1
            if self._is_valid_move(x1, y1, set()):
                path.append((x1, y1))
            else:
                break
        
        return path
    
    def _build_path_from_tree(self, node: TreeNode) -> List[Tuple[int, int]]:
        path = []
        current = node
        while current:
            path.append((current.x, current.y))
            current = current.parent
        return path[::-1]
    
    def solve(self):
        start_time = time.time()
        root = TreeNode(self.start[0], self.start[1])
        queue = Queue()
        queue.enqueue(self.start[0], self.start[1])
        visited = {self.start}
        
        while queue.size > 0:
            current = queue.dequeue()
            if not current:
                continue
                
            x, y = current
            current_node = root
            
            # Si llegamos al final, guardamos la solución
            if (x, y) == self.end:
                path = self._build_path_from_tree(current_node)
                self.solutions.append(Solution(
                    path=path,
                    time_found=time.time() - start_time,
                    length=len(path)
                ))
                continue
            
            # Animar la tortuga retornando al inicio
            if self.current_turtle != self.start:
                self._animate_turtle_movement(self.current_turtle, self.start)
                self.current_turtle = self.start
            
            # Explorar movimientos posibles
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._is_valid_move(nx, ny, visited):
                    visited.add((nx, ny))
                    queue.enqueue(nx, ny)
                    new_node = TreeNode(nx, ny, current_node)
                    current_node.children.append(new_node)
                    
                    # Animar el movimiento de la tortuga
                    self._animate_turtle_movement(self.current_turtle, (nx, ny))
                    self.current_turtle = (nx, ny)
        
        self._print_statistics()
    
    def _print_statistics(self):
        if not self.solutions:
            print("No se encontraron soluciones")
            return
            
        shortest = min(self.solutions, key=lambda x: x.length)
        longest = max(self.solutions, key=lambda x: x.length)
        avg_time = sum(sol.time_found for sol in self.solutions) / len(self.solutions)
        
        print("\nEstadísticas:")
        print(f"Total de soluciones encontradas: {len(self.solutions)}")
        print(f"\nSolución más corta (longitud {shortest.length}):")
        self._print_solution(shortest.path)
        print(f"Tiempo para encontrar: {shortest.time_found:.2f} segundos")
        
        print(f"\nSolución más larga (longitud {longest.length}):")
        self._print_solution(longest.path)
        print(f"Tiempo para encontrar: {longest.time_found:.2f} segundos")
        
        print(f"\nTiempo promedio: {avg_time:.2f} segundos")
    
    def _print_solution(self, path: List[Tuple[int, int]]):
        maze_copy = [[cell for cell in row] for row in self.maze]
        for x, y in path:
            if (x, y) != self.start and (x, y) != self.end:
                maze_copy[x][y] = 'o'
        
        print("+" + "-" * (self.size * 3) + "+")
        for row in maze_copy:
            print("|", end=" ")
            for cell in row:
                print(f"{cell} ", end=" ")
            print("|")
        print("+" + "-" * (self.size * 3) + "+")

def main():
    size = int(input("Ingrese el tamaño del laberinto (n x n): "))
    maze_string = input(f"Ingrese el laberinto como una cadena de {size*size} caracteres: ")
    delay = int(input("Ingrese el retraso entre pasos (milisegundos): "))
    
    if len(maze_string) != size * size:
        print(f"Error: La cadena debe tener exactamente {size*size} caracteres")
        return
    
    solver = MazeSolver(size, maze_string, delay)
    solver.solve()

if __name__ == "__main__":
    main()