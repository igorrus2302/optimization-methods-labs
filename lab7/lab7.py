from math import inf

C = [
    [inf, 98, 69, 66, 95, 70, 17, 64,  4, 18],
    [  2, inf, 77, 11, 81, 36, 25,  6, 73, 93],
    [ 68, 78, inf, 25, 81, 84, 14, 47, 36, 96],
    [ 50, 48, 20, inf, 23, 24, 51, 44, 80, 23],
    [ 77, 51, 77, 33, inf, 66, 85, 21, 15, 95],
    [ 13, 88, 47, 83, 61, inf, 40,  2,  4, 48],
    [ 89, 68, 68, 76, 45, 39, inf, 48, 26, 56],
    [ 79, 49, 16, 17, 11, 73,  4, inf,  2, 28],
    [ 84, 50, 30, 67, 61, 95, 85, 74, inf, 22],
    [ 89, 87, 51, 90, 83, 81, 57, 19, 74, inf]
]

labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def tsp_branch_and_bound(cost_matrix, start=0):
    n = len(cost_matrix)
    all_visited_mask = (1 << n) - 1

    best_cost = [inf]
    best_path = [[]]

    def dfs(current, visited_mask, path, cost_so_far):
        if cost_so_far >= best_cost[0]:
            return

        if visited_mask == all_visited_mask:
            tour_cost = cost_so_far + cost_matrix[current][start]
            if tour_cost < best_cost[0]:
                best_cost[0] = tour_cost
                best_path[0] = path[:] + [start]
            return

        for nxt in range(n):
            if nxt == start:
                continue
            if not (visited_mask & (1 << nxt)):
                new_cost = cost_so_far + cost_matrix[current][nxt]
                dfs(nxt, visited_mask | (1 << nxt), path + [nxt], new_cost)

    dfs(start, 1 << start, [start], 0.0)

    return best_cost[0], best_path[0]


if __name__ == "__main__":
    best_cost, best_path = tsp_branch_and_bound(C, start=0)

    print("Минимальная длина маршрута:", best_cost)

    labeled_path = " → ".join(labels[i] for i in best_path)
    print("Маршрут:", labeled_path)
