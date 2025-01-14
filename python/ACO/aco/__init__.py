import matplotlib.pyplot as plt
import numpy as np
from ant import Ant
import random


class AntColony:
    def __init__(
        self,
        graph,  # Объект класса Graph
        start_node=0,  # Начальный узел для поиска пути
        ant_count=10,  # Количество муравьев в колонии
        alpha=1.0,  # Параметр alpha для феромонов
        beta=2.0,  # Параметр beta для эвристической информации
        pheromone_evaporation_rate=0.3,  # Скорость испарения феромонов
        pheromone_constant=1.0,  # Константа феромонов
        iterations=100,  # Количество итераций алгоритма
    ):
        """
        Инициализация алгоритма колонии муравьев с заданными параметрами.
        
        :param graph: Граф, в котором будет происходить поиск пути.
        :param start_node: Начальный узел для поиска пути.
        :param ant_count: Количество муравьев в колонии.
        :param alpha: Параметр alpha для феромонов.
        :param beta: Параметр beta для эвристической информации.
        :param pheromone_evaporation_rate: Скорость испарения феромонов.
        :param pheromone_constant: Константа феромонов.
        :param iterations: Количество итераций для выполнения алгоритма.
        """
        self.graph = graph  # Граф для поиска
        self.start_node = start_node  # Начальный узел
        self.ant_count = ant_count  # Количество муравьев
        self.alpha = alpha  # Параметр феромонов
        self.beta = beta    # Параметр эвристической информации
        self.pheromone_evaporation_rate = pheromone_evaporation_rate  # Скорость испарения феромонов
        self.pheromone_constant = pheromone_constant  # Константа феромонов
        self.iterations = iterations  # Количество итераций

        self.num_nodes = len(graph.nodes)  # Количество узлов в графе
        self.pheromone_map = {
            (i, j): 1 for i in graph.nodes for j in graph.get_neighbors(i)
        }  # Инициализация карты феромонов

        self.tmp_pheromone_map = {
            (i, j): 0 for i in graph.nodes for j in graph.get_neighbors(i)
        }  # Временная карта феромонов для обновления

        self.best_path = None  # Лучший найденный путь
        self.best_cost = float('inf')  # Стоимость лучшего пути
        self.path_lengths = [float('inf')] * self.iterations  # Длины путей на каждой итерации
        self.best_path_probabilities = []  # Вероятности для лучшего пути на каждой итерации

    def run(self):
        """
        Запуск алгоритма колонии муравьев. Итерирует по количеству итераций,
        строит решения для каждого муравья и обновляет феромоны.
        
        :return: Лучший путь и его стоимость.
        """
        ants = [Ant(alpha=self.alpha, beta=self.beta) for _ in range(self.ant_count)]  # Создаем муравьев

        for iteration in range(self.iterations):  # Проходим по итерациям
            iteration_best_cost = float('inf')  # Наилучшая стоимость пути для текущей итерации
            successful_paths = 0  # Количество успешных путей

            best_path_probability = 0  # Вероятность для лучшего пути в текущей итерации

            for ant in ants:  # Строим пути для каждого муравья
                ant.reset(self.start_node)  # Сбрасываем муравья для новой итерации
                success, path_cost = self.construct_solution(ant)  # Строим решение

                if success:
                    successful_paths += 1  # Увеличиваем количество успешных путей
                    if path_cost < self.best_cost:
                        iteration_best_cost = path_cost
                        self.best_cost = iteration_best_cost
                        self.best_path = ant.route  # Обновляем лучший путь

            self.path_lengths[iteration] = self.best_cost  # Сохраняем стоимость лучшего пути на итерации
            self.update_pheromones()  # Обновляем феромоны

            if self.best_path:
                best_path_probability = self.calculate_best_path_probability()  # Рассчитываем вероятность лучшего пути
            self.best_path_probabilities.append(best_path_probability)  # Добавляем вероятность в список

            self.update_pheromones()  # Еще раз обновляем феромоны

        return self.best_path, self.best_cost  # Возвращаем лучший путь и его стоимость

    def construct_solution(self, ant):
        """
        Строит решение для муравья, проходя через все узлы графа.
        
        :param ant: Муравей, для которого строится решение.
        :return: True, если решение успешно, иначе False и бесконечная стоимость.
        """
        current_node = self.start_node  # Начинаем с начального узла

        while len(ant.visited) < self.num_nodes:  # Пока все узлы не посещены
            next_node = self.choose_next_node(ant, current_node)  # Выбираем следующий узел
            if next_node is None:  # Если нет доступных узлов для перехода, завершаем
                return False, float('inf')

            ant.route.append(next_node)  # Добавляем узел в маршрут
            ant.visited.add(next_node)  # Добавляем узел в множество посещенных
            current_node = next_node  # Переходим в следующий узел

        # Завершаем маршрут, если есть путь к стартовому узлу
        if self.graph.get_weight(current_node, self.start_node) < float('inf'):
            ant.route.append(self.start_node)  # Добавляем стартовый узел в маршрут
            path_cost = self.calculate_path_cost(ant.route)  # Вычисляем стоимость пути
            self.update_tmp_pheromones(ant.route, path_cost)  # Обновляем временные феромоны
            return True, path_cost

        return False, float('inf')  # Если не удалось завершить путь, возвращаем бесконечную стоимость

    def choose_next_node(self, ant, current_node):
        """
        Выбирает следующий узел для муравья на основе вероятностей, пропорциональных феромонам и эвристике.
        
        :param ant: Муравей, для которого выбирается следующий узел.
        :param current_node: Текущий узел муравья.
        :return: Следующий узел, или None, если нет доступных для перехода.
        """
        probabilities = []  # Список вероятностей для перехода к соседям
        total_probability = 0  # Общая вероятность для нормализации

        for neighbor, weight in self.graph.get_neighbors(current_node).items():  # Проходим по соседям
            if neighbor in ant.visited:  # Если сосед уже посещен, пропускаем его
                continue

            pheromone = self.pheromone_map[(current_node, neighbor)]  # Считываем феромон на ребре
            heuristic = 1 / weight  # Эвристическая информация (например, 1/вес ребра)
            probability = (pheromone ** self.alpha) * (heuristic ** self.beta)  # Вычисляем вероятность

            probabilities.append((neighbor, probability))  # Добавляем вероятность для соседа
            total_probability += probability  # Суммируем общую вероятность

        if not probabilities:  # Если нет доступных соседей, возвращаем None
            return None

        random_choice = random.uniform(0, total_probability)  # Выбираем случайное число в пределах общей вероятности
        cumulative_probability = 0  # Переменная для накопления вероятности

        for neighbor, probability in probabilities:
            cumulative_probability += probability  # Накопление вероятности
            if cumulative_probability >= random_choice:  # Если накопленная вероятность больше или равна случайному числу
                return neighbor  # Возвращаем выбранного соседа

        return None  # Если не удалось выбрать соседа, возвращаем None

    def calculate_path_cost(self, path):
        """
        Вычисляет стоимость пути, суммируя веса всех ребер в маршруте.
        
        :param path: Маршрут (список узлов).
        :return: Стоимость пути.
        """
        cost = 0  # Начальная стоимость пути
        for i in range(len(path) - 1):  # Проходим по всем ребрам в пути
            cost += self.graph.get_weight(path[i], path[i + 1])  # Суммируем вес ребра
        return cost  # Возвращаем стоимость пути

    def update_tmp_pheromones(self, path, path_cost):
        """
        Обновляет временную карту феромонов на основе найденного пути и его стоимости.
        
        :param path: Маршрут муравья.
        :param path_cost: Стоимость найденного пути.
        """
        for i in range(len(path) - 1):  # Проходим по всем ребрам в пути
            a, b = path[i], path[i + 1]
            self.tmp_pheromone_map[(a, b)] += self.pheromone_constant / path_cost  # Увеличиваем феромон
            self.tmp_pheromone_map[(b, a)] += self.pheromone_constant / path_cost  # Симметрично для обратного ребра

    def update_pheromones(self):
        """
        Обновляет карту феромонов, учитывая испарение феромонов и новые данные.
        """
        for edge in self.pheromone_map:
            self.pheromone_map[edge] *= (1 - self.pheromone_evaporation_rate)  # Испаряем феромоны
            self.pheromone_map[edge] += self.tmp_pheromone_map[edge]  # Добавляем новые феромоны
            self.tmp_pheromone_map[edge] = 0  # Очищаем временную карту феромонов

    def plot_graphs(self):
        """
        Строит график длин путей на протяжении всех итераций.
        """
        path_lengths_no_inf = [np.nan if length == float('inf') else length for length in self.path_lengths]
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, self.iterations + 1), path_lengths_no_inf, color='orange')  # График длины пути
        plt.title('Path Lengths Over Iterations')  # Заголовок графика
        plt.xlabel('Iteration')  # Подпись оси X
        plt.ylabel('Path Length')  # Подпись оси Y
        plt.tight_layout()  # Автоматически подстраиваем layout
        plt.grid()  # Включаем сетку
        plt.show()  # Отображаем график

    def calculate_best_path_probability(self):
        """
        Рассчитывает вероятность того, что лучший путь будет выбран на основе феромонов и эвристики.
        
        :return: Вероятность для лучшего пути.
        """
        probability = 1.0  # Начальная вероятность
        for i in range(len(self.best_path) - 1):  # Проходим по всем ребрам лучшего пути
            a, b = self.best_path[i], self.best_path[i + 1]
            pheromone = self.pheromone_map.get((a, b), 1)  # Считываем феромон
            weight = self.graph.get_weight(a, b)  # Получаем вес ребра
            heuristic = 1 / weight  # Эвристическая информация (обратный вес)
            probability *= (pheromone ** self.alpha) * (heuristic ** self.beta)  # Обновляем вероятность
        return probability  # Возвращаем итоговую вероятность
    
    def plot_best_path_probability(self):
        """
        Строит график вероятности лучшего пути на протяжении всех итераций.
        """
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, self.iterations + 1), self.best_path_probabilities, color='green')  # График вероятности
        plt.title('Best Path Probability Over Iterations')  # Заголовок графика
        plt.xlabel('Iteration')  # Подпись оси X
        plt.ylabel('Best Path Probability')  # Подпись оси Y
        plt.tight_layout()  # Автоматически подстраиваем layout
        plt.grid()  # Включаем сетку
        plt.show()  # Отображаем график