import itertools
from heapq import heappush, heappop

class Graph:
    """
    Представляет граф с использованием списков смежности.

    Атрибуты:
        adjacency_list (dict): Словарь, где ключи — объекты Vertex, 
        а значения — списки объектов Edge, представляющих связи и их веса.
    """
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list


class Vertex:
    """
    Представляет вершину (узел) в графе.

    Атрибуты:
        value (any): Уникальный идентификатор вершины, например, строка или число.
    """
    def __init__(self, value):
        self.value = value


class Edge:
    """
    Представляет ребро, соединяющее две вершины в графе.

    Атрибуты:
        distance (float): Вес ребра.
        vertex (Vertex): Вершина, к которой ведет это ребро.
    """
    def __init__(self, distance, vertex):
        self.distance = distance
        self.vertex = vertex


def dijkstra(graph, start, end):
    """
    Реализация алгоритма Дейкстры для нахождения кратчайшего пути в графе с весами.

    Аргументы:
        graph (Graph): Граф, представленный списком смежности из вершин и ребер.
        start (Vertex): Стартовая вершина.
        end (Vertex): Конечная вершина, до которой нужно найти кратчайший путь.

    Логика работы:
    1. Инициализация:
        - 'previous': Словарь для отслеживания предшественников каждой вершины в кратчайшем пути.
        - 'visited': Словарь для отметки, была ли вершина полностью обработана.
        - 'distances': Словарь с минимально известными расстояниями от стартовой вершины до каждой вершины.
    2. Устанавливается расстояние до стартовой вершины равным 0, остальные — бесконечность.
    3. Используется очередь с приоритетами для выбора вершины с минимальным известным расстоянием.
    4. Для каждого соседа текущей вершины:
        - Если сосед ещё не посещён, рассчитывается новое расстояние через текущую вершину.
        - Если это расстояние меньше ранее известного, оно обновляется.
        - Записывается предшественник для восстановления пути.
    5. Обработка завершается, когда достигается конечная вершина или очередь становится пустой.
    6. Кратчайший путь восстанавливается с использованием словаря 'previous'.

    Выводит:
        - Кратчайшее расстояние до конечной вершины.
        - Последовательность вершин, образующих кратчайший путь.

    Возвращает:
        None
    """
    previous = {v: None for v in graph.adjacency_list.keys()}
    visited = {v: False for v in graph.adjacency_list.keys()}
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0
    queue = PriorityQueue()
    queue.add_task(0, start)
    path = []
    while queue:
        removed_distance, removed = queue.pop_task()
        visited[removed] = True

        if removed is end:
            while previous[removed]:
                path.append(removed.value)
                removed = previous[removed]
            path.append(start.value)
            print(f"Кратчайшее расстояние до {end.value}: ", distances[end])
            print(f"Путь до {end.value}: ", path[::-1])
            return

        for edge in graph.adjacency_list[removed]:
            if visited[edge.vertex]:
                continue
            new_distance = removed_distance + edge.distance
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                queue.add_task(new_distance, edge.vertex)
    return

class PriorityQueue:
    """
    Очередь с приоритетом, реализованная с использованием кучи (min-heap) для 
    эффективного извлечения задач с наименьшим приоритетом.

    Атрибуты:
        pq (list): Список элементов, организованных в виде кучи, где каждая запись — 
        это список [priority, count, task].
        entry_finder (dict): Словарь для быстрого доступа к элементам кучи по задаче.
        counter (itertools.count): Уникальный счётчик для разрешения конфликтов приоритетов.

    Методы:
        add_task(priority, task):
            Добавляет новую задачу или обновляет приоритет существующей.
        update_priority(priority, task):
            Обновляет приоритет существующей задачи.
        pop_task():
            Извлекает и возвращает задачу с наименьшим приоритетом.
        __len__():
            Возвращает количество задач в очереди.
    """
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def __len__(self):
        """
        Возвращает количество задач в очереди.
        """
        return len(self.pq)

    def add_task(self, priority, task):
        """
        Добавляет новую задачу в очередь или обновляет приоритет существующей.

        Аргументы:
            priority (float): Приоритет задачи, где меньшие значения означают более высокий приоритет.
            task (any): Задача, которую нужно добавить или обновить.

        Если задача уже существует, её приоритет обновляется.
        """
        if task in self.entry_finder:
            self.update_priority(priority, task)
            return self
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def update_priority(self, priority, task):
        """
        Обновляет приоритет существующей задачи.

        Аргументы:
            priority (float): Новое значение приоритета для задачи.
            task (any): Задача, для которой нужно обновить приоритет.
        """
        entry = self.entry_finder[task]
        count = next(self.counter)
        entry[0], entry[1] = priority, count

    def pop_task(self):
        """
        Удаляет и возвращает задачу с наименьшим приоритетом из очереди.

        Возвращает:
            tuple: Кортеж (priority, task) для задачи с минимальным приоритетом.

        Исключения:
            KeyError: Если очередь пуста.
        """
        while self.pq:
            priority, count, task = heappop(self.pq)
            del self.entry_finder[task]
            return priority, task
        raise KeyError('pop from an empty priority queue')


# Тестирование алгоритма
vertices = [Vertex("A"), Vertex("B"), Vertex("C"), Vertex("D"), Vertex("E"), Vertex("F"), Vertex("G"), Vertex("H")]
A, B, C, D, E, F, G, H = vertices

adj_list = {
    A: [Edge(1.8, B), Edge(1.5, C), Edge(1.4, D)],
    B: [Edge(1.8, A), Edge(1.6, E)],
    C: [Edge(1.5, A), Edge(1.8, E), Edge(2.1, F)],
    D: [Edge(1.4, A), Edge(2.7, F), Edge(2.4, G)],
    E: [Edge(1.6, B), Edge(1.8, C), Edge(1.4, F), Edge(1.6, H)],
    F: [Edge(2.1, C), Edge(2.7, D), Edge(1.4, E), Edge(1.3, G), Edge(1.2, H)],
    G: [Edge(2.4, D), Edge(1.3, F), Edge(1.5, H)],
    H: [Edge(1.6, E), Edge(1.2, F), Edge(1.5, G)],
}

my_graph = Graph(adj_list)

dijkstra(my_graph, start=A, end=H)