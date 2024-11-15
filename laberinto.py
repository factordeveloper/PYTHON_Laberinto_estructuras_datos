import time
import os
from colorama import Fore, Back, Style, init


class Node:
    def __init__(self, x, y, next=None, prev=None):
        self.x = x
        self.y = y
        self.next = next
        self.prev = prev

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
    
    def push(self, x, y):
        new_node = Node(x, y)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
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
    
    def enqueue(self, x, y):
        new_node = Node(x, y)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
        self.size += 1
    
    def dequeue(self):
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
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.children = []

class Solution:
    def __init__(self, path, time_found, length):
        self.path = path
        self.time_found = time_found
        self.length = length

class MazeSolver:
    def __init__(self, size, maze_string, delay_ms):
        self.size = size
        self.maze = [list(maze_string[i:i+size]) for i in range(0, len(maze_string), size)]
        self.delay = delay_ms / 1000
        self.start = self._find_position('0')
        self.end = self._find_position('X')
        self.solutions = []
        self.current_position = self.start
        self.start_time = time.time()
    
    def _find_position(self, char):
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == char:
                    return (i, j)
        return (-1, -1)
    
    def _is_valid_move(self, x, y, visited):
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                self.maze[x][y] != '+' and 
                (x, y) not in visited)
    
    def _move_to(self, x, y, visited):
        old_x, old_y = self.current_position
        
        if self.maze[old_x][old_y] not in ['0', 'X']:
            if (old_x, old_y) in visited:
                self.maze[old_x][old_y] = 'o'
            else:
                self.maze[old_x][old_y] = ' '
        
        self.current_position = (x, y)
        if self.maze[x][y] not in ['0', 'X']:
            self.maze[x][y] = '@'
        
        self._print_maze()
    
    def _print_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * (self.size * 4) + "+")
        for i in range(self.size):
            print("|", end=" ")
            for j in range(self.size):
                cell = self.maze[i][j]
                if (i, j) == self.current_position and cell not in ['0', 'X']:
                    print("@", end="  ")
                else:
                    print(f"{cell}", end="  ")
            print("|")
        print("+" + "-" * (self.size * 4) + "+")
        time.sleep(self.delay)
    
    def solve(self):
        if not self._verify_maze():
            print("El laberinto no es válido o no tiene solución posible.")
            return
        
        self._find_all_solutions()
        self._print_final_statistics()
    
    def _verify_maze(self):
        return (self.start != (-1, -1) and 
                self.end != (-1, -1) and 
                self.start != self.end)
    
    def _find_all_solutions(self):
        stack = Stack()
        stack.push(self.start[0], self.start[1])
        visited = {self.start}
        path = [self.start]
        
        while stack.size > 0:
            x, y = stack.pop() or (0, 0)
            self._move_to(x, y, visited)
            
            if (x, y) == self.end:
                solution_time = time.time() - self.start_time
                self.solutions.append(Solution(
                    path=path.copy(),
                    time_found=solution_time,
                    length=len(path)
                ))
                if len(path) > 1:
                    path.pop()
                    visited.remove((x, y))
                continue
            
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self._is_valid_move(nx, ny, visited):
                    neighbors.append((nx, ny))
            
            if not neighbors:
                if len(path) > 1:
                    path.pop()
                    if (x, y) not in [self.start, self.end]:
                        visited.remove((x, y))
                continue
            
            for nx, ny in neighbors:
                stack.push(nx, ny)
                visited.add((nx, ny))
                path.append((nx, ny))
    
    def _print_final_statistics(self):
        if not self.solutions:
            print("\nNo se encontraron soluciones.")
            return
        
        shortest = min(self.solutions, key=lambda x: x.length)
        longest = max(self.solutions, key=lambda x: x.length)
        avg_time = sum(sol.time_found for sol in self.solutions) / len(self.solutions)
        
        print("\nEstadísticas finales:")
        print(f"Número total de soluciones encontradas: {len(self.solutions)}")
        
        print("\nSolución más corta:")
        print(f"Longitud: {shortest.length} pasos")
        print(f"Tiempo: {shortest.time_found:.3f} segundos")
        self._print_solution(shortest.path)
        
        print("\nSolución más larga:")
        print(f"Longitud: {longest.length} pasos")
        print(f"Tiempo: {longest.time_found:.3f} segundos")
        self._print_solution(longest.path)
        
        print(f"\nTiempo promedio para encontrar solución: {avg_time:.3f} segundos")
    
    def _print_solution(self, path):
        solution_maze = [[cell for cell in row] for row in self.maze]
        for x, y in path:
            if (x, y) not in [self.start, self.end]:
                solution_maze[x][y] = 'o'
        
        print("+" + "-" * (self.size * 4) + "+")
        for row in solution_maze:
            print("|", end=" ")
            for cell in row:
                print(f"{cell}", end="  ")
            print("|")
        print("+" + "-" * (self.size * 4) + "+")

def main():
    size = int(input("Ingrese el tamaño del laberinto (n x n): "))
    print("\nUse los siguientes caracteres:")
    print("0: Posición inicial")
    print("X: Posición final")
    print("+: Paredes (No transitables)")
    print("  (espacio): Celdas transitables")
    maze_string = input(f"\nIngrese el laberinto como una cadena de {size*size} caracteres: ")
    delay = int(input("Ingrese el retraso entre pasos (milisegundos): "))
    
    if len(maze_string) != size * size:
        print(f"Error: La cadena debe tener exactamente {size*size} caracteres")
        return
    
    solver = MazeSolver(size, maze_string, delay)
    solver.solve()

if __name__ == "__main__":
    main()