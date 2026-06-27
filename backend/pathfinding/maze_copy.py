import sys

class Node():
    # Данные клетки
    # state - координаты клетки
    # parent - для поиска пути обратно
    def __init__(self, state, parent, action):
        self.state = state 
        self.parent = parent
        self.action = action

    def valuate(self, value, parent_path_value):
        self.value = value
        self.path_value = parent_path_value + 1

class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    """DFS - Depth-First Search"""
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    """BFS - Breadth-First Search"""
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Bidirectional(StackFrontier):
    ...

class GreedyFrontier(QueueFrontier):
    def __init__(self):
        self.frontier = []
        self.values = []

    def add(self, node):
        path_value = node.parent.path_value
        ...

class Maze():
    def __init__(self, filename, algorithm):
        # Прочитать файл с пазлом
        with open(filename) as f:
            contents = f.read()

        match algorithm :
            case "bfs":
                self.frontier_class  = QueueFrontier
            case "dfs":
                self.frontier_class  = StackFrontier
            case _:
                raise Exception("wrong algorithm")

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
        
        self.solution = None

    def print(self):
        # Если solution найдено, брать только решение, иначе None
        if self.solution is not None:
            solution = self.solution[1]
            explored = self.explored
        else: 
            solution, explored = None, None
        
        # Система вывода в консоль
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # col - проверка на стену (True/False)
                if col:
                    print("█", end="")
                
                # start
                elif (i, j) == self.start:
                    print("A", end="")

                # goal
                elif (i, j) == self.goal:
                    print("B", end="")

                # Если есть solution, проводит путь
                # Иначе, рисует maze без решения
                elif solution is not None:
                    if (i, j) in solution:
                        print('*', end="")
                    elif (i, j) in explored:
                        print("-", end="")
                    else:
                        print(" ", end="")
                # Пустые клетки
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state # текущая клетка
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]

        # Проверить какие клетки доступны для action
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r,c)))
        return result

    def solve(self):
        """Находит решение пазла, если он существует"""

        # Счетчик изученных клеток
        self.num_explored = 0

        # Создаём frontier для двух сторон и добавляем стартовую и целевую клетку
        start = Node(state=self.start, parent=None, action=None)
        start_frontier = self.frontier_class()
        start_frontier.add(start)

        goal = Node(state=self.goal, parent=None, action=None)
        goal_frontier = self.frontier_class()
        goal_frontier.add(goal)

        # Создать пустое хранилище изученных клеток
        # Цель: не проверять уже изученные клетки
        self.explored = set()

        while True:

            # Если изучили все возможные клетки для любого frontier, выводит ошибку
            if start_frontier.empty() or goal_frontier.empty():
                raise Exception("no solution")

            # Достать следующую клетку для изучения
            node = start_frontier.remove()
            self.num_explored += 1

            print(start_frontier.frontier)
            # Если клетка является выходом, значит мы нашли решение
            if node.state == self.goal:
                actions = []
                cells = []
                # Ищем начальную клетку
                # Ex: Идем с конца по ссылкам parent, у начальной клетки parent = None
                while node.parent is not None:
                    actions.append(node.action) # Сохраняем действие
                    cells.append(node.state) # Сохраняем координаты
                    node = node.parent # Заменяем, и идем дальше

                # Переворачиваем массивы, получается путь с начала до конца
                actions.reverse()
                cells.reverse()

                # Сохраняем решение, и завершаем solve
                self.solution = (actions, cells)
                return

            # Сохраняем координаты клетки как изученная
            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

argv_len = len(sys.argv)
if argv_len != 3:
    sys.exit("Usage: python maze.py maze.txt dfs")

# Инициализация
maze = Maze(sys.argv[1], sys.argv[2])

# Вывод начального пазла
print("Maze:")
maze.print()

# Процесс решения
print("Solving...")
maze.solve()

# Вывод решения пазла
print("Solution:")
maze.print()