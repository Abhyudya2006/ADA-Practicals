def matrix_chain_order(p):
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # Dynamic Programming to fill tables
    for l in range(2, n + 1):  # l = chain length
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        print(f"A{i}", end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")


def main():
    print("--- Matrix Chain Multiplication Solver ---")
    try:
        user_input = input("Enter dimensions separated by spaces: ")
        p = list(map(int, user_input.split()))

        if len(p) < 2:
            print("Error: Provide at least 2 dimensions.")
            return

        n = len(p) - 1
        m_table, s_table = matrix_chain_order(p)

        # Output Section
        print("\n" + "=" * 50)
        print(f"{'Matrix Range':<20} | {'Min Cost':<12} | {'Split (k)':<10}")
        print("-" * 50)

        # Print correct subproblem costs
        for l in range(2, n + 1):
            for i in range(1, n - l + 2):
                j = i + l - 1
                print(f"A{i} to A{j:<13} | {m_table[i][j]:<12} | {s_table[i][j]:<10}")

        print("-" * 50)

        print("Optimal Parenthesization: ", end="")
        print_optimal_parens(s_table, 1, n)

        print(f"\nMinimum Scalar Multiplications: {m_table[1][n]}")
        print("=" * 50)

    except ValueError:
        print("Invalid input. Please enter numbers only.")


if __name__ == "__main__":
    main()