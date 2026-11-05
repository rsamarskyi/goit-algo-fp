"""Завдання 6. Жадібні алгоритми та динамічне програмування.

Вибір страв з максимальною сумарною калорійністю в межах бюджету.
"""

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int) -> dict:
    """Жадібний алгоритм: беремо страви за спаданням calories/cost,
    поки вистачає бюджету. Складність: O(n log n).
    Не гарантує оптимального результату."""
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen = []
    total_cost = 0
    total_calories = 0

    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]

    return {"items": chosen, "cost": total_cost, "calories": total_calories}


def dynamic_programming(items: dict, budget: int) -> dict:
    """Динамічне програмування (рюкзак 0/1).

    dp[i][b] — максимум калорій, який можна отримати, використовуючи
    перші i страв при бюджеті b. Складність: O(n * budget).
    Гарантує оптимальний результат (вартості — цілі числа).
    """
    names = list(items.keys())
    n = len(names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        cal = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо страву i
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + cal)  # беремо

    # Відновлення набору страв
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    return {"items": chosen, "cost": total_cost, "calories": dp[n][budget]}


if __name__ == "__main__":
    for budget in (30, 60, 100, 150):
        print(f"--- Бюджет: {budget} ---")
        g = greedy_algorithm(items, budget)
        d = dynamic_programming(items, budget)
        print(f"Жадібний:  {g['items']}, вартість={g['cost']}, калорії={g['calories']}")
        print(f"Динамічний: {d['items']}, вартість={d['cost']}, калорії={d['calories']}")
        print()