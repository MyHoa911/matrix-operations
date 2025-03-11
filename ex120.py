import numpy as np

def generate_matrix(N, M):
    return np.random.randint(-100, 101, (N, M))

def calculate_determinant(matrix):
    if matrix.shape[0] == matrix.shape[1]:
        return np.linalg.det(matrix)
    else:
        return "Determinant is only defined for square matrices."

def inverse_matrix(matrix):
    if matrix.shape[0] == matrix.shape[1]:
        try:
            return np.linalg.inv(matrix)
        except np.linalg.LinAlgError:
            return "Matrix is singular and cannot be inverted."
    else:
        return "Inverse is only defined for square matrices."

def sort_matrix_by_row(matrix):
    return np.sort(matrix, axis=1)

def sort_matrix_by_column(matrix):
    return np.sort(matrix, axis=0)

def sort_matrix_by_row_avg(matrix):
    row_avg = np.mean(matrix, axis=1)
    sorted_indices = np.argsort(row_avg)
    return matrix[sorted_indices]

def modify_element(matrix, row, col, new_value):
    matrix[row, col] = new_value
    return matrix

def modify_column(matrix, col):
    matrix[:, col] += 2
    return matrix

def add_vector_to_rows(matrix, vector):
    return matrix + vector

def calculate_rank(matrix):
    return np.linalg.matrix_rank(matrix)

def singular_value_decomposition(matrix):
    U, S, V = np.linalg.svd(matrix)
    return U, S, V

# Example usage
N, M = 4, 4  # Example size, can be changed
matrix = generate_matrix(N, M)
print("Original Matrix:")
print(matrix)

# Determinant and Inverse (if applicable)
print("\nDeterminant:", calculate_determinant(matrix))
print("\nInverse Matrix:")
print(inverse_matrix(matrix))

# Sorting
print("\nMatrix sorted by row:")
print(sort_matrix_by_row(matrix))
print("\nMatrix sorted by column:")
print(sort_matrix_by_column(matrix))
print("\nMatrix sorted by row average:")
print(sort_matrix_by_row_avg(matrix))

# Modify element
matrix = modify_element(matrix, 1, 2, 999)
print("\nModified Matrix (Element Changed):")
print(matrix)

# Modify column
matrix = modify_column(matrix, 2)
print("\nModified Matrix (Column Increased by 2):")
print(matrix)

# Adding a vector
vector = np.random.randint(-10, 10, (1, M))
matrix = add_vector_to_rows(matrix, vector)
print("\nMatrix after adding a vector:")
print(matrix)

# Matrix Rank
print("\nMatrix Rank:", calculate_rank(matrix))

# SVD
U, S, V = singular_value_decomposition(matrix)
print("\nMatrix U:")
print(U)
print("\nSingular values S:")
print(S)
print("\nMatrix V:")
print(V)
