def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    mirror = []
    for item in matrix:
        mirror.append(item[::-1])
    return mirror