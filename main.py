import numpy as np

# дано
costs = np.array([
    [2, 6, 3, 4],
    [4, 7, 7, 2],
    [8, 3, 1, 7],
    [5, 4, 6, 1],
    [9, 3, 7, 7]
])

supply = [54, 87, 59, 192, 35]
demand = [179, 131, 34, 83]

m, n = costs.shape

# метод северо-западного угла
def northwest_corner(supply, demand):
    supply = supply.copy()
    demand = demand.copy()

    x = np.zeros((m, n), dtype=int)

    i = 0
    j = 0

    while i < m and j < n:
        amount = min(supply[i], demand[j])
        x[i, j] = amount

        supply[i] -= amount
        demand[j] -= amount

        if supply[i] == 0 and i < m - 1:
            i += 1
        elif demand[j] == 0 and j < n - 1:
            j += 1
        else:
            break

    return x

# метод минимальных значений
def least_cost_method(costs, supply, demand):
    supply = supply.copy()
    demand = demand.copy()
    x = np.zeros((m, n), dtype=int)

    # список всех клеток (стоимость, i, j)
    cells = [(costs[i][j], i, j) for i in range(m) for j in range(n)]
    cells.sort()  # сортируем по стоимости

    for c, i, j in cells:
        if supply[i] == 0 or demand[j] == 0:
            continue

        amount = min(supply[i], demand[j])
        x[i][j] = amount
        supply[i] -= amount
        demand[j] -= amount

    return x


# метод потенциалов
def calculate_potentials(x, costs):
    """Вычисление потенциалов u_i, v_j по базисным клеткам."""
    m, n = x.shape
    u = [None] * m
    v = [None] * n

    u[0] = 0

    changed = True
    while changed:
        changed = False
        for i in range(m):
            for j in range(n):
                if x[i][j] > 0:  # базисная клетка
                    if u[i] is not None and v[j] is None:
                        v[j] = costs[i][j] - u[i]
                        changed = True
                    elif u[i] is None and v[j] is not None:
                        u[i] = costs[i][j] - v[j]
                        changed = True
    return u, v


def modi_method(costs, supply, demand):
    x = northwest_corner(supply, demand)

    while True:
        u, v = calculate_potentials(x, costs)

        # считаем оценки Δ(i,j)
        delta = np.full_like(costs, 0, dtype=int)
        min_delta = 0
        enter_cell = None

        for i in range(m):
            for j in range(n):
                if x[i][j] == 0:
                    delta[i][j] = costs[i][j] - u[i] - v[j]
                    if delta[i][j] < min_delta:
                        min_delta = delta[i][j]
                        enter_cell = (i, j)

        # если нет отрицательных Δ — оптимум
        if enter_cell is None:
            return x

        ei, ej = enter_cell

        # строим цикл
        from collections import deque
        cycle = []

        def find_cycle(start_i, start_j):
            """Поиск цикла (упрощённый вариант)."""
            # По строке
            for jj in range(n):
                if x[start_i][jj] > 0 and jj != start_j:
                    # По столбцу
                    for ii in range(m):
                        if x[ii][jj] > 0 and ii != start_i:
                            if x[ii][start_j] > 0 or (ii == start_i and start_j == jj):
                                return [(start_i, start_j),
                                        (start_i, jj),
                                        (ii, jj),
                                        (ii, start_j)]
            return None

        cycle = find_cycle(ei, ej)
        if cycle is None:
            return x

        # расставляем знаки + -
        plus = cycle[0::2]
        minus = cycle[1::2]

        # ищем θ
        theta = min(x[i][j] for i, j in minus)

        # пересчёт
        for i, j in plus:
            x[i][j] += theta
        for i, j in minus:
            x[i][j] -= theta

        # удаляем нули, чтобы поддерживать базис
        for i, j in minus:
            if x[i][j] == 0:
                x[i][j] = 0

    return x

X1 = northwest_corner(supply, demand)
X2 = least_cost_method(costs, supply, demand)
X3 = modi_method(costs, supply, demand)

print("Метод северо-западного угла:\n", X1)
print("\nМетод минимальных значений:\n", X2)
print("\nОптимальный план методом потенциалов:\n", X3)
