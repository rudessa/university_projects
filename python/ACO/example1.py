import matplotlib.pyplot as plt
from aco import AntColony
import matplotlib.pyplot as plt
from aco import AntColony
from graph import Graph

# Создаем граф
graph = Graph()

# Добавляем ребра в граф
edges = [
    (0, 1, 3),  # Ребро между вершинами 0 и 1 с весом 3
    (0, 4, 1),  # Ребро между вершинами 0 и 4 с весом 1
    (1, 2, 18), # Ребро между вершинами 1 и 2 с весом 18
    (1, 5, 3),  # Ребро между вершинами 1 и 5 с весом 3
    (2, 3, 1),  # Ребро между вершинами 2 и 3 с весом 1
    (2, 5, 1),  # Ребро между вершинами 2 и 5 с весом 1
    (3, 4, 1),  # Ребро между вершинами 3 и 4 с весом 1
    (3, 5, 5),  # Ребро между вершинами 3 и 5 с весом 5
    (4, 5, 4)   # Ребро между вершинами 4 и 5 с весом 4
]

for edge in edges:
    graph.add_edge(*edge)

# Настраиваем муравьиную колонию
colony = AntColony(
    graph=graph,
    start_node=0,
    ant_count=1,
    iterations=60,
    alpha=2,
    beta=1,
    pheromone_evaporation_rate=0.3,
    pheromone_constant=0.5
)

# Запуск алгоритма
best_path, best_cost = colony.run()

# Вывод результатов
print(f"Best path: {best_path}")
print(f"Best cost: {best_cost}")

# Построение графиков
colony.plot_graphs()