"""Завдання 7. Метод Монте-Карло: кидання двох кубиків.

Симулюємо N кидків двох кубиків, рахуємо частоту кожної суми (2..12),
оцінюємо ймовірності та порівнюємо їх з аналітичними (кількість
сприятливих комбінацій / 36).
"""

import random
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SUMS = list(range(2, 13))


def analytic_probabilities() -> dict:
    """Аналітичні ймовірності: P(s) = (6 - |s - 7|) / 36."""
    return {s: (6 - abs(s - 7)) / 36 for s in SUMS}


def monte_carlo(n_rolls: int, seed: int | None = None) -> dict:
    """Імітація n_rolls кидків двох кубиків; повертає {сума: ймовірність}."""
    rng = random.Random(seed)
    counts = Counter(rng.randint(1, 6) + rng.randint(1, 6) for _ in range(n_rolls))
    return {s: counts[s] / n_rolls for s in SUMS}


def print_table(mc: dict, analytic: dict, n_rolls: int) -> None:
    print(f"Кількість кидків: {n_rolls:,}\n")
    print(f"{'Сума':>4} | {'Монте-Карло':>12} | {'Аналітична':>11} | {'Різниця, в.п.':>13}")
    print("-" * 52)
    for s in SUMS:
        diff = (mc[s] - analytic[s]) * 100
        print(f"{s:>4} | {mc[s]:>11.2%} | {analytic[s]:>10.2%} | {diff:>+13.3f}")
    max_dev = max(abs(mc[s] - analytic[s]) for s in SUMS) * 100
    print(f"\nМаксимальне відхилення: {max_dev:.3f} в.п.")


def plot(mc: dict, analytic: dict, n_rolls: int, path: str) -> None:
    width = 0.4
    xs = SUMS
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([x - width / 2 for x in xs], [mc[s] * 100 for s in xs], width,
           label=f"Монте-Карло (N = {n_rolls:,})", color="#4C78A8")
    ax.bar([x + width / 2 for x in xs], [analytic[s] * 100 for s in xs], width,
           label="Аналітична", color="#F58518")
    ax.set_xticks(xs)
    ax.set_xlabel("Сума на двох кубиках")
    ax.set_ylabel("Імовірність, %")
    ax.set_title("Імовірності сум при киданні двох кубиків")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def convergence(analytic: dict) -> None:
    """Як максимальне відхилення залежить від кількості кидків."""
    print("\nЗбіжність (максимальне відхилення від аналітичних значень):")
    for n in (100, 1_000, 10_000, 100_000, 1_000_000):
        mc = monte_carlo(n, seed=42)
        dev = max(abs(mc[s] - analytic[s]) for s in SUMS) * 100
        print(f"  N = {n:>9,}: {dev:.3f} в.п.")


if __name__ == "__main__":
    N = 1_000_000
    analytic = analytic_probabilities()
    mc = monte_carlo(N, seed=42)
    print_table(mc, analytic, N)
    convergence(analytic)
    plot(mc, analytic, N, "dice_probabilities.png")
    print("\nГрафік збережено: dice_probabilities.png")