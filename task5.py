import heapq
import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="#D3D3D3"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def heap_to_tree(heap):
    """Створює дерево зі списку без рекурсії."""
    if not heap:
        return None

    nodes = [Node(value) for value in heap]

    for i, node in enumerate(nodes):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(nodes):
            node.left = nodes[left]

        if right < len(nodes):
            node.right = nodes[right]

    return nodes[0]


def prepare_graph(root):
    """Створює граф і координати вузлів без рекурсії."""
    graph = nx.DiGraph()
    positions = {}
    nodes = {}

    stack = [(root, 0, 0, 1)]

    while stack:
        node, x, y, layer = stack.pop()

        graph.add_node(node.id, label=node.val)
        positions[node.id] = (x, y)
        nodes[node.id] = node

        if node.right is not None:
            graph.add_edge(node.id, node.right.id)
            stack.append((
                node.right,
                x + 1 / 2 ** layer,
                y - 1,
                layer + 1
            ))

        if node.left is not None:
            graph.add_edge(node.id, node.left.id)
            stack.append((
                node.left,
                x - 1 / 2 ** layer,
                y - 1,
                layer + 1
            ))

    return graph, positions, nodes


def visit_color(step, total):
    """Повертає унікальний HEX-колір від темного до світлого."""
    ratio = step / max(total - 1, 1)

    red = round(18 + (180 - 18) * ratio)
    green = round(50 + (220 - 50) * ratio)
    blue = round(100 + (255 - 100) * ratio)

    return f"#{red:02X}{green:02X}{blue:02X}"


def draw_step(ax, graph, positions, nodes, title):
    ax.clear()

    labels = nx.get_node_attributes(graph, "label")
    colors = [nodes[node_id].color for node_id in graph.nodes]

    nx.draw(
        graph,
        pos=positions,
        labels=labels,
        node_color=colors,
        node_size=2000,
        font_color="white",
        edgecolors="black",
        arrows=False,
        ax=ax
    )

    ax.set_title(title)


def visualize_traversal(root, method, delay=1):
    if root is None:
        print("Дерево порожнє")
        return

    if method not in ("DFS", "BFS"):
        raise ValueError("Оберіть DFS або BFS")

    graph, positions, nodes = prepare_graph(root)

    # Скидаємо кольори перед кожним обходом.
    for node in nodes.values():
        node.color = "#D3D3D3"

    fig, ax = plt.subplots(figsize=(9, 6))
    draw_step(ax, graph, positions, nodes, f"{method}: початок")
    plt.show(block=False)
    plt.pause(delay)

    order = []

    # Для DFS використовуємо стек, для BFS — чергу.
    pending = [root] if method == "DFS" else deque([root])

    while pending:
        if not plt.fignum_exists(fig.number):
            break

        if method == "DFS":
            node = pending.pop()
        else:
            node = pending.popleft()

        node.color = visit_color(len(order), len(nodes))
        order.append(node.val)

        draw_step(
            ax,
            graph,
            positions,
            nodes,
            f"{method}: крок {len(order)}, відвідано {node.val}"
        )
        plt.pause(delay)

        if method == "DFS":
            # Правого додаємо першим, щоб лівого відвідати раніше.
            if node.right is not None:
                pending.append(node.right)
            if node.left is not None:
                pending.append(node.left)
        else:
            if node.left is not None:
                pending.append(node.left)
            if node.right is not None:
                pending.append(node.right)

    print(f"{method}: {order}")
    plt.show()


if __name__ == "__main__":
    heap = [10, 4, 5, 0, 1, 3, 8, 7]
    heapq.heapify(heap)

    root = heap_to_tree(heap)

    visualize_traversal(root, "DFS")
    visualize_traversal(root, "BFS")