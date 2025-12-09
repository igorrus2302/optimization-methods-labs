def print_table(title, header, rows):
    print("\n" + title)
    print("-" * max(40, 6 * len(header)))
    print("".join(f"{h:>6}" for h in header))
    for row in rows:
        print("".join(f"{c:>6}" for c in row))
    print("-" * max(40, 6 * len(header)))


def solve_resource_allocation(profits, total_resource):
    n = len(profits)
    R = total_resource

    dp = [[0] * (R + 1) for _ in range(n + 1)]
    decision = [[0] * (R + 1) for _ in range(n + 1)]

    for k in range(1, n + 1):
        for s in range(0, R + 1):
            best_value = -10**9
            best_x = 0
            max_x = min(s, len(profits[k - 1]) - 1)
            for x in range(0, max_x + 1):
                value = profits[k - 1][x] + dp[k - 1][s - x]
                if value > best_value:
                    best_value = value
                    best_x = x
            dp[k][s] = best_value
            decision[k][s] = best_x

    allocation = [0] * n
    s = R
    for k in range(n, 0, -1):
        x = decision[k][s]
        allocation[k - 1] = x
        s -= x

    max_profit = dp[n][R]
    return dp, decision, allocation, max_profit


def main():
    profits = [
        [0, 2, 2, 3, 5, 8, 9],
        [0, 1, 1, 1, 2, 3, 4],
        [0, 2, 2, 3, 5, 5, 8],
        [0, 1, 4, 6, 9, 9, 9],
        [0, 1, 3, 5, 7, 7, 7],
        [0, 2, 5, 6, 7, 7, 8],  
    ]
    total_resource = 6

    n = len(profits)

    header = ["P\\x"] + [str(j) for j in range(0, total_resource + 1)]
    rows = []
    for i in range(n):
        row = [f"P{i+1}"] + [profits[i][j] for j in range(0, total_resource + 1)]
        rows.append(row)
    print_table("Таблица прибыли f_i(x)", header, rows)

    dp, decision, allocation, max_profit = solve_resource_allocation(profits, total_resource)

    dp_header = ["k\\s"] + [str(s) for s in range(0, total_resource + 1)]
    dp_rows = []
    for k in range(1, n + 1):
        row = [f"{k}"] + [dp[k][s] for s in range(0, total_resource + 1)]
        dp_rows.append(row)
    print_table("Таблица значений F_k(s)", dp_header, dp_rows)

    dec_rows = []
    for k in range(1, n + 1):
        row = [f"{k}"] + [decision[k][s] for s in range(0, total_resource + 1)]
        dec_rows.append(row)
    print_table("Таблица решений x_k*(s)", dp_header, dec_rows)

    print("\nОПТИМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ РЕСУРСА")
    print("=" * 40)
    for i, x in enumerate(allocation, start=1):
        print(f"Предприятие P{i}: {x} ед. ресурса")
    print("-" * 40)
    print(f"Максимальная суммарная прибыль: {max_profit}")
    print("=" * 40)


if __name__ == "__main__":
    main()
