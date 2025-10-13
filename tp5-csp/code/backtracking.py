def backtracking_n_queens(N, seed=None):
    import random
    if seed is not None:
        random.seed(seed)

    soluciones = []
    nodos = 0
    found = False

    def es_valida(asignacion, fila, col):
        for f_anterior in range(fila):
            c_anterior = asignacion[f_anterior]
            if c_anterior == col or abs(c_anterior - col) == abs(f_anterior - fila):
                return False
        return True

    def resolver(asignacion, fila):
        nonlocal nodos, found
        if found:
            return True
        if fila == N:
            soluciones.append(asignacion.copy())
            found = True
            return True

        columnas = list(range(N))
        if seed is not None:
            random.shuffle(columnas)

        for col in columnas:
            nodos += 1
            if es_valida(asignacion, fila, col):
                asignacion[fila] = col
                if resolver(asignacion, fila + 1):
                    return True  # cortar al encontrar una solución
                asignacion[fila] = -1
        return False

    resolver([-1] * N, 0)
    return soluciones, nodos
