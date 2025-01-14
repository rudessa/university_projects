from node import Node  # Импортируем класс Node, который используется для представления узлов графа


class Graph:
    def __init__(self):
        """
        Инициализация графа с пустым словарем узлов.
        """
        self.nodes = {}  # Словарь для хранения узлов графа

    def add_node(self, node_id):
        """
        Добавляет узел в граф по его идентификатору.
        
        :param node_id: Идентификатор узла, который нужно добавить.
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)  # Создаем новый узел и добавляем его в граф

    def add_edge(self, node1_id, node2_id, weight):
        """
        Добавляет ребро между двумя узлами с указанным весом.
        
        :param node1_id: Идентификатор первого узла.
        :param node2_id: Идентификатор второго узла.
        :param weight: Вес ребра между узлами.
        """
        self.add_node(node1_id)  # Убедимся, что узлы добавлены в граф
        self.add_node(node2_id)
        self.nodes[node1_id].add_edge(node2_id, weight)  # Добавляем ребро в первый узел
        self.nodes[node2_id].add_edge(node1_id, weight)  # Добавляем ребро во второй узел

    def get_neighbors(self, node_id):
        """
        Возвращает соседей для указанного узла.
        
        :param node_id: Идентификатор узла, для которого нужно получить соседей.
        :return: Словарь соседей узла с весами ребер.
        """
        return self.nodes[node_id].edges  # Возвращаем словарь соседей узла

    def get_weight(self, node1_id, node2_id):
        """
        Возвращает вес ребра между двумя узлами.
        
        :param node1_id: Идентификатор первого узла.
        :param node2_id: Идентификатор второго узла.
        :return: Вес ребра между узлами или бесконечность, если ребра нет.
        """
        return self.nodes[node1_id].edges.get(node2_id, float('inf'))  # Возвращаем вес ребра или бесконечность
