class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def from_list(items):
    """Build a linked list from a Python list, return the head."""
    head = None
    for x in reversed(items):
        node = Node(x)
        node.next = head
        head = node
    return head


def to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


def reverse(head):
    """Reverse the links between nodes, return the new head."""
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def insertion_sort(head):
    """Take nodes one by one and insert each into the sorted result."""
    sorted_head = None
    while head:
        node = head
        head = head.next
        if sorted_head is None or node.data < sorted_head.data:
            node.next = sorted_head
            sorted_head = node
        else:
            cur = sorted_head
            while cur.next and cur.next.data <= node.data:
                cur = cur.next
            node.next = cur.next
            cur.next = node
    return sorted_head


def merge_sorted(a, b):
    """Merge two sorted lists into one sorted list."""
    dummy = Node(None)
    tail = dummy
    while a and b:
        if a.data <= b.data:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


if __name__ == "__main__":
    head = from_list([1, 2, 3, 4, 5])
    head = reverse(head)
    print("reversed:", to_list(head))
    assert to_list(head) == [5, 4, 3, 2, 1]

    head = insertion_sort(from_list([7, 3, 9, 1, 5, 3, 8]))
    print("sorted:  ", to_list(head))
    assert to_list(head) == [1, 3, 3, 5, 7, 8, 9]

    merged = merge_sorted(from_list([1, 4, 6, 10]), from_list([2, 3, 7, 11, 12]))
    print("merged:  ", to_list(merged))
    assert to_list(merged) == [1, 2, 3, 4, 6, 7, 10, 11, 12]

    assert to_list(reverse(None)) == []
    assert to_list(merge_sorted(None, from_list([1, 2]))) == [1, 2]
    print("All checks passed.")