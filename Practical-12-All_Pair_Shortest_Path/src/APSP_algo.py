import sys

INF = float('inf')

class AllPairShortestPath:
    def get_input_matrix(self, n):
        """Helper to collect matrix input from the user."""
        print(f"\nEnter the cost matrix row by row (space-separated values).")
        print("Type 'INF' for infinity.")
        
        matrix = []
        for i in range(n):
            while True:
                try:
                    row_input = input(f"Row {i+1}: ").split()
                    if len(row_input) != n:
                        raise ValueError(f"Expected {n} values, got {len(row_input)}.")
                    
                    # Convert inputs to float, handling 'INF'
                    row = [INF if val.upper() == 'INF' else float(val) for val in row_input]
                    matrix.append(row)
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please try again.")
        return matrix

    def print_matrix(self, matrix, n):
        """Helper to print the matrix in a readable format."""
        for i in range(n):
            row_str = []
            for j in range(n):
                val = "INF" if matrix[i][j] == INF else f"{int(matrix[i][j]):>3}"
                row_str.append(val)
            print("  ".join(row_str))
        print("-" * (n * 5))

    def solve_with_iterations(self, cost, n):
        """
        Implements Floyd-Warshall and prints only when the matrix is updated.
        """
        # Initialize A with the input cost matrix
        A = [row[:] for row in cost]
        
        print("\n--- Starting Iterations ---")
        print("Initial Matrix (A0):")
        self.print_matrix(A, n)

        # Main algorithm loops
        for k in range(n):
            updated_in_this_step = False
            print(f"Checking via vertex {k+1}...")

            for i in range(n):
                for j in range(n):
                    # Check if a shorter path exists through vertex k
                    if A[i][k] + A[k][j] < A[i][j]:
                        A[i][j] = A[i][k] + A[k][j]
                        updated_in_this_step = True
            
            # Only show the matrix if an update actually occurred
            if updated_in_this_step:
                print(f"Matrix updated (Iter k={k+1}):")
                self.print_matrix(A, n)
            else:
                print(f"No updates via vertex {k+1}.\n")

        print("Final Shortest Path Matrix:")
        self.print_matrix(A, n)
        return A

def main():
    obj = AllPairShortestPath()
    
    try:
        n_input = input("Enter the number of vertices: ")
        n = int(n_input)
        
        graph = obj.get_input_matrix(n)
        obj.solve_with_iterations(graph, n)
        
    except ValueError:
        print("Error: Please enter a valid integer for the number of vertices.")
    except KeyboardInterrupt:
        print("\nProgram terminated.")

if __name__ == "__main__":
    main()