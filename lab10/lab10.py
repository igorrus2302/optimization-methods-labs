def main():
    S = 10

    weights = [1, 2, 3, 4, 5, 6]
    values  = [1, 4, 7, 10, 9, 8]

    n = len(weights)

    print("-" * 60)
    print(f"Грузоподъёмность рюкзака: S = {S}")
    print("Тип предмета:    ", " ".join(f"{i:3d}" for i in range(1, n + 1)))
    print("Вес a_i:          ", " ".join(f"{w:3d}" for w in weights))
    print("Ценность v_i:     ", " ".join(f"{v:3d}" for v in values))
    print("-" * 60)

    W_tables = []
    X_tables = []

    W_prev = [0] * (S + 1)

    for k in range(1, n + 1):
        a_k = weights[k - 1]
        v_k = values[k - 1]

        W_cur = [0] * (S + 1)
        X_cur = [0] * (S + 1)

        for C in range(0, S + 1):
            best_value = W_prev[C]
            best_x = 0

            max_x = C // a_k

            for x in range(1, max_x + 1):
                value = x * v_k + W_prev[C - x * a_k]
                if value > best_value:
                    best_value = value
                    best_x = x

            W_cur[C] = best_value
            X_cur[C] = best_x

        W_tables.append(W_cur)
        X_tables.append(X_cur)
        W_prev = W_cur

    def print_step_table(k, Wk, Xk):
        print(f"\nШаг {k}. Учитываются предметы типов 1..{k}")
        print(f"Вес a_{k} = {weights[k-1]}, ценность v_{k} = {values[k-1]}")
        print("C:        " + " ".join(f"{C:3d}" for C in range(0, S + 1)))
        print(f"W_{k}(C): " + " ".join(f"{val:3d}" for val in Wk))
        print(f"x_{k}(C): " + " ".join(f"{x:3d}" for x in Xk))

    for k in range(1, n + 1):
        print_step_table(k, W_tables[k - 1], X_tables[k - 1])

    optimal_value = W_tables[-1][S]

    x_opt = [0] * n
    C = S
    for k in range(n, 0, -1):
        x_k = X_tables[k - 1][C]
        x_opt[k - 1] = x_k
        C -= x_k * weights[k - 1]

    total_weight = sum(w * x for w, x in zip(weights, x_opt))
    total_value = sum(v * x for v, x in zip(values, x_opt))

    print("\n" + "=" * 60)
    print("ИТОГОВОЕ РЕШЕНИЕ")
    print("=" * 60)
    print(f"Максимальная суммарная ценность W*(S={S}) = {optimal_value}")
    print("\nОптимальные количества предметов (x_i):")
    print("Тип i:         ", " ".join(f"{i:3d}" for i in range(1, n + 1)))
    print("Оптимальный x_i:", " ".join(f"{x:3d}" for x in x_opt))

    print("\nПроверка ограничения по весу:")
    print(f"Суммарный вес  = {total_weight} (не должен превышать S = {S})")
    print(f"Суммарная ценность = {total_value}")

    print("\nИнтерпретация решения:")
    for i, (w, v, x) in enumerate(zip(weights, values, x_opt), start=1):
        if x > 0:
            print(f" - взять {x} шт. предмета типа {i} "
                  f"(вес {w}, ценность {v} каждый)")
    if all(x == 0 for x in x_opt):
        print(" - ни один предмет не выбран (тривиальное решение)")


if __name__ == "__main__":
    main()
