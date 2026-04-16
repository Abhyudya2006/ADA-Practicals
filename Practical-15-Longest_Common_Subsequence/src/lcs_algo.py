def lcs_algorithm(X, Y):
    m = len(X)
    n = len(Y)
    
    # c[i][j] stores the length of LCS of X[0..i-1] and Y[0..j-1]
    # b[i][j] stores directions: '↖' (Match), '↑' (Up), '←' (Left)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[""] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = "↖"
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = "↑"
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = "←"
                
    return c, b

def get_lcs(b, X, i, j):
    if i == 0 or j == 0:
        return ""
    if b[i][j] == "↖":
        return get_lcs(b, X, i-1, j-1) + X[i-1]
    elif b[i][j] == "↑":
        return get_lcs(b, X, i-1, j)
    else:
        return get_lcs(b, X, i, j-1)

def main():
    print("--- Longest Common Subsequence (LCS) Solver ---")
    s1 = input("Enter first sequence: ").strip()
    s2 = input("Enter second sequence: ").strip()

    c_table, b_table = lcs_algorithm(s1, s2)

    print("\nLCS Length Matrix (c):")
    for row in c_table:
        print("  ".join(map(str, row)))

    print("\nDirection Matrix (b):")
    for row in b_table:
        print("  ".join([(cell if cell else ".") for cell in row]))

    lcs_string = get_lcs(b_table, s1, len(s1), len(s2))
    
    print("\n" + "="*30)
    print(f"Final LCS: {lcs_string}")
    print(f"LCS Length: {c_table[len(s1)][len(s2)]}")
    print("="*30)

if __name__ == "__main__":
    main()