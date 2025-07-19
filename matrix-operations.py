import numpy as np

def get_matrix_input(matrix_name):
    """
    Prompts the user to input the dimensions and elements of a matrix.
    Args:
        matrix_name (str): A descriptive name for the matrix (e.g., "Matrix A").
    Returns:
        numpy.ndarray: The matrix entered by the user.
    """
    print(f"\n--- Enter {matrix_name} ---")
    while True:
        try:
            rows = int(input(f"Enter the number of rows for {matrix_name}: "))
            cols = int(input(f"Enter the number of columns for {matrix_name}: "))
            if rows <= 0 or cols <= 0:
                print("Number of rows and columns must be positive integers. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter integers for dimensions.")

    matrix_elements = []
    print(f"Enter the elements for {matrix_name} row by row (space-separated):")
    for i in range(rows):
        while True:
            try:
                row_str = input(f"Row {i + 1}: ")
                row_elements = list(map(float, row_str.split()))
                if len(row_elements) != cols:
                    print(f"Incorrect number of elements. Expected {cols}, got {len(row_elements)}. Please re-enter the row.")
                else:
                    matrix_elements.append(row_elements)
                    break
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
    return np.array(matrix_elements)

def display_matrix(matrix, title="Matrix"):
    """
    Displays a NumPy matrix in a structured format.
    Args:
        matrix (numpy.ndarray): The matrix to display.
        title (str): A title for the matrix display.
    """
    print(f"\n--- {title} ---")
    if matrix.size == 0:
        print("Empty Matrix")
    else:
        print(matrix)
    print("-" * (len(title) + 8)) # Decorative line

def main():
    """
    Main function for the Matrix Operations Tool.
    Manages user interaction, operation selection, and result display.
    """
    print("Welcome to the Matrix Operations Tool!")

    while True:
        print("\n--- Choose an Operation ---")
        print("1. Addition (A + B)")
        print("2. Subtraction (A - B)")
        print("3. Multiplication (A * B)")
        print("4. Transpose (A^T)")
        print("5. Determinant (det(A))")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            matrix_a = get_matrix_input("Matrix A")
            matrix_b = get_matrix_input("Matrix B")
            if matrix_a.shape != matrix_b.shape:
                print("\nError: Matrices must have the same dimensions for addition.")
            else:
                result = matrix_a + matrix_b
                display_matrix(matrix_a, "Matrix A")
                display_matrix(matrix_b, "Matrix B")
                display_matrix(result, "Result of Addition (A + B)")

        elif choice == '2':
            matrix_a = get_matrix_input("Matrix A")
            matrix_b = get_matrix_input("Matrix B")
            if matrix_a.shape != matrix_b.shape:
                print("\nError: Matrices must have the same dimensions for subtraction.")
            else:
                result = matrix_a - matrix_b
                display_matrix(matrix_a, "Matrix A")
                display_matrix(matrix_b, "Matrix B")
                display_matrix(result, "Result of Subtraction (A - B)")

        elif choice == '3':
            matrix_a = get_matrix_input("Matrix A")
            matrix_b = get_matrix_input("Matrix B")
            # For matrix multiplication A * B, number of columns in A must equal number of rows in B
            if matrix_a.shape[1] != matrix_b.shape[0]:
                print("\nError: For matrix multiplication (A * B), the number of columns in Matrix A must equal the number of rows in Matrix B.")
            else:
                result = np.dot(matrix_a, matrix_b) # or matrix_a @ matrix_b in Python 3.5+
                display_matrix(matrix_a, "Matrix A")
                display_matrix(matrix_b, "Matrix B")
                display_matrix(result, "Result of Multiplication (A * B)")

        elif choice == '4':
            matrix_a = get_matrix_input("Matrix A")
            result = np.transpose(matrix_a)
            display_matrix(matrix_a, "Original Matrix A")
            display_matrix(result, "Result of Transpose (A^T)")

        elif choice == '5':
            matrix_a = get_matrix_input("Matrix A")
            if matrix_a.shape[0] != matrix_a.shape[1]:
                print("\nError: Determinant can only be calculated for square matrices.")
            else:
                try:
                    result = np.linalg.det(matrix_a)
                    display_matrix(matrix_a, "Matrix A")
                    print(f"\n--- Determinant of Matrix A ---")
                    print(f"det(A) = {result:.4f}") # Format to 4 decimal places
                    print("-----------------------------")
                except np.linalg.LinAlgError as e:
                    print(f"\nError calculating determinant: {e}. This might happen for singular matrices.")

        elif choice == '6':
            print("Exiting Matrix Operations Tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...") # Pause for user to read output

if __name__ == "__main__":
    main()
