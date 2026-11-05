import uuid
import heapq

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # колір вузла
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.show()


def heap_to_tree(heap, index=0):
    """Рекурсивно перетворює масив-купу на дерево з вузлів Node.

    Зв'язок індексів у купі, що зберігається в списку:
        лівий нащадок  -> 2 * i + 1
        правий нащадок -> 2 * i + 2
    """
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def draw_heap(heap):
    """Візуалізує бінарну купу (список у форматі heapq / масиву купи)."""
    if not heap:
        print("Купа порожня")
        return
    root = heap_to_tree(heap)
    draw_tree(root)


if __name__ == "__main__":
    # Min-heap, побудована за допомогою heapq
    min_heap = []
    for value in [10, 4, 5, 0, 1, 3, 8, 7]:
        heapq.heappush(min_heap, value)
    print("Min-heap:", min_heap)
    draw_heap(min_heap)

    # Max-heap: зберігаємо значення з протилежним знаком
    max_heap = []
    for value in [10, 4, 5, 0, 1, 3, 8, 7]:
        heapq.heappush(max_heap, -value)
    draw_heap([-v for v in max_heap])