import folium
import osmnx as ox


class RoutePlanner:
    def __init__(self):
        self.listeners = []  # Список подписчиков
        self.route_length = 0  # Длина маршрута

    def add_listener(self, listener):
        """Добавить подписчика на событие."""
        self.listeners.append(listener)

    def _notify_listeners(self, message):
        """Уведомить всех подписчиков."""
        for listener in self.listeners:
            listener(message)

    def calculate_route(self, start_coords, end_coords, output_file="route_map.html"):
        """
        Рассчитать маршрут и сохранить карту в HTML.

        :param start_coords: Координаты начала пути [широта, долгота].
        :param end_coords: Координаты конца пути [широта, долгота].
        :param output_file: Имя файла для сохранения HTML-карты.

        :return: Длина маршрута в метрах.
        """
        print("Ожидайте +-10 секунд ...")

        # Создаем карту
        mymap = folium.Map(location=start_coords, zoom_start=7)

        # Получаем граф уличной сети
        G = ox.graph_from_point(start_coords, dist=50000, network_type='drive')

        # Находим узлы ближайшие к старту и финишу
        orig_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
        dest_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])

        # Вычисляем маршрут
        route = ox.shortest_path(G, orig_node, dest_node, weight='length')

        # Преобразуем маршрут в координаты
        route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]

        # Выводим прогресс построения маршрута
        for i, node in enumerate(route):
            message = f"Построен участок маршрута: узел {i + 1} с координатами {G.nodes[node]['y'], G.nodes[node]['x']}"
            print(message)
            self._notify_listeners(message)  # Уведомить подписчиков

        # Рассчитываем длину маршрута
        self.route_length = 0
        for i in range(len(route) - 1):
            edge_data = G.get_edge_data(route[i], route[i + 1])
            if edge_data:
                self.route_length += edge_data[0]['length']  # берем длину первого рёбра

        print(f"Длина маршрута: {self.route_length:.2f} метров")

        # Добавляем маршрут на карту
        folium.PolyLine(locations=route_coords, color='red', weight=5, opacity=0.7).add_to(mymap)

        # Добавляем маркеры для начальной и конечной точки
        folium.Marker(location=start_coords, popup='Начало', icon=folium.Icon(color='blue')).add_to(mymap)
        folium.Marker(location=end_coords, popup='Конец', icon=folium.Icon(color='green')).add_to(mymap)

        # Сохраняем карту в HTML файл
        mymap.save(output_file)

        return self.route_length

