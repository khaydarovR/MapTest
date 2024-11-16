from route_planner import RoutePlanner


class ProgressListener:
    def __call__(self, message):
        print(f"Событие: {message}")


if __name__ == "__main__":
    planner = RoutePlanner()

    # Подписка на события
    listener = ProgressListener()
    planner.add_listener(listener)

    # Задаем координаты
    start_coords = [55.757453, 52.434443]  # Набережные Челны
    end_coords = [55.633855, 51.842825]  # Нижнекамск

    # Рассчитываем маршрут и получаем длину
    route_length = planner.calculate_route(start_coords, end_coords, output_file="route_map.html")

    print(f"Общая длина маршрута: {route_length:.2f} метров")
