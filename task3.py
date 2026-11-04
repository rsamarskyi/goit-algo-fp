import heapq


def dijkstra(graph, start):
    """Знаходить найкоротші відстані від початкової вершини."""
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0

    # Бінарна мінімальна купа: (відстань, вершина).
    heap = [(0, start)]

    while heap:
        current_distance, current_vertex = heapq.heappop(heap)

        # Пропускаємо запис, якщо вже знайдено коротший шлях.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances


if __name__ == "__main__":
    # Неорієнтований зважений граф.
    # Кожне ребро записане в обох напрямках.
    graph = {
        "A": {"B": 4, "C": 1},
        "B": {"A": 4, "C": 2, "D": 1},
        "C": {"A": 1, "B": 2, "D": 5},
        "D": {"B": 1, "C": 5, "E": 3},
        "E": {"D": 3},
        "F": {},  # Недосяжна вершина.
    }

    start = "A"
    distances = dijkstra(graph, start)

    print(f"Найкоротші відстані від вершини {start}:")

    for vertex, distance in distances.items():
        if distance == float("inf"):
            print(f"{start} → {vertex}: немає шляху")
        else:
            print(f"{start} → {vertex}: {distance}")

    assert distances == {
        "A": 0,
        "B": 3,
        "C": 1,
        "D": 4,
        "E": 7,
        "F": float("inf"),
    }