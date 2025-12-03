def hungarian_algorithm(cost):
    n = len(cost)
    c = [row[:] for row in cost]

    for i in range(n):
        row_min = min(c[i])
        for j in range(n):
            c[i][j] -= row_min

    for j in range(n):
        col_min = min(c[i][j] for i in range(n))
        for i in range(n):
            c[i][j] -= col_min

    def find_zero_cover_and_matching(c):
        n = len(c)
        zeros_in_row = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if c[i][j] == 0:
                    zeros_in_row[i].append(j)

        match_to_row = [-1] * n

        def dfs(i, seen):
            for j in zeros_in_row[i]:
                if seen[j]:
                    continue
                seen[j] = True
                if match_to_row[j] == -1 or dfs(match_to_row[j], seen):
                    match_to_row[j] = i
                    return True
            return False

        match_count = 0
        for i in range(n):
            seen = [False] * n
            if dfs(i, seen):
                match_count += 1

        full = (match_count == n)

        matched_row = [False] * n
        for j in range(n):
            if match_to_row[j] != -1:
                matched_row[match_to_row[j]] = True

        from collections import deque
        row_marked = [False] * n
        col_marked = [False] * n
        q = deque()

        for i in range(n):
            if not matched_row[i]:
                row_marked[i] = True
                q.append(("row", i))

        while q:
            kind, idx = q.popleft()
            if kind == "row":
                i = idx
                for j in zeros_in_row[i]:
                    if not col_marked[j]:
                        col_marked[j] = True
                        q.append(("col", j))
            else:
                j = idx
                i = match_to_row[j]
                if i != -1 and not row_marked[i]:
                    row_marked[i] = True
                    q.append(("row", i))

        cover_rows = [not row_marked[i] for i in range(n)]
        cover_cols = [col_marked[j] for j in range(n)]
        return full, cover_rows, cover_cols, match_to_row

    while True:
        full, cover_rows, cover_cols, match_to_row = find_zero_cover_and_matching(c)
        if full:
            assignment = [-1] * n
            for j, i in enumerate(match_to_row):
                if i != -1:
                    assignment[i] = j
            total_cost = sum(cost[i][assignment[i]] for i in range(n))
            return assignment, total_cost

        min_uncovered = None
        for i in range(n):
            for j in range(n):
                if not cover_rows[i] and not cover_cols[j]:
                    v = c[i][j]
                    if min_uncovered is None or v < min_uncovered:
                        min_uncovered = v

        for i in range(n):
            for j in range(n):
                if not cover_rows[i] and not cover_cols[j]:
                    c[i][j] -= min_uncovered
                elif cover_rows[i] and cover_cols[j]:
                    c[i][j] += min_uncovered


def solve_and_pretty_print():
    cost = [
        [9, 2, 5, 7, 6, 5, 7, 2, 2, 9],
        [8, 8, 6, 6, 2, 8, 2, 8, 7, 1],
        [5, 6, 3, 3, 7, 2, 2, 2, 4, 4],
        [1, 7, 1, 2, 7, 9, 9, 5, 8, 8],
        [4, 7, 2, 6, 4, 5, 3, 7, 4, 6],
        [2, 2, 1, 9, 8, 4, 2, 8, 7, 5],
        [4, 1, 4, 3, 2, 4, 8, 7, 6, 9],
        [3, 2, 8, 3, 7, 7, 9, 8, 6, 8],
        [8, 4, 9, 4, 1, 6, 6, 6, 1, 9],
        [3, 5, 3, 7, 5, 8, 2, 2, 9, 1],
    ]
    n = len(cost)

    def print_matrix(title, m):
        print(title)
        print(" " * 6 + " ".join(f"j{j+1:>3}" for j in range(len(m[0]))))
        for i, row in enumerate(m):
            print(f"i{i+1:>2}: " + " ".join(f"{val:>4}" for val in row))
        print()

    print_matrix("Матрица затрат C (исходная):", cost)

    assignment, total_cost = hungarian_algorithm(cost)

    print("Оптимальное назначение (строка → столбец):")
    print("-" * 50)
    print(f"{'Работник':>10} | {'Работа':>10} | {'Стоимость':>10}")
    print("-" * 50)
    for i in range(n):
        j = assignment[i]
        print(f"{i+1:>10} | {j+1:>10} | {cost[i][j]:>10}")
    print("-" * 50)
    print(f"Минимальная суммарная стоимость: {total_cost}")
    print()

    print("Матрица назначений X (1 – выбрано, 0 – иначе):")
    x = [[0] * n for _ in range(n)]
    for i in range(n):
        x[i][assignment[i]] = 1
    print_matrix("X:", x)


if __name__ == "__main__":
    solve_and_pretty_print()
