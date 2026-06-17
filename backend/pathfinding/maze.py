import sys

class Node():
    # Данные клетки
    # state - координаты клетки
    # parent - для поиска пути обратно
    def __init__(self, state, parent, action):
        self.state = state 
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else: ## why not use pop?
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
    
        # Прочитать файл с пазлом
        with open(filename) as f:
            contents = f.read()

        # Получить height и width пазла
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Identify start and goal
        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError: ## Why?
                    row.append(False) 
            self.walls.append(row)
        print(self.walls)
        print(self.height, self.width)

    def neighbors(self, state):
        row, col = state    # текущая клетка
        candidates = [
            ("up", (row-1, col))
            ("down", (row+1, col))
            ("left", (row, col-1))
            ("right", (row, col+1))
        ]

        # Проверить какие клетки доступны для action
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r,c)))
        return result


Maze("maze1.txt")