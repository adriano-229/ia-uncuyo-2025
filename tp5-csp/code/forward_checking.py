def forward_checking_n_queens(N, seed=None):
    import random
    if seed is not None:
        random.seed(seed)

    soluciones = []
    nodos = 0
    found = False

    def fc(asignacion, dominios, fila):
        nonlocal nodos, found
        if found:
            return True
        if fila == N:
            soluciones.append(asignacion.copy())
            found = True
            return True

        valores = dominios[fila][:]
        if seed is not None:
            random.shuffle(valores)

        for col in valores:
            nodos += 1
            asignacion[fila] = col
            nuevos_dominios = [d.copy() for d in dominios]
            consistente = True
            for f in range(fila + 1, N):
                if col in nuevos_dominios[f]:
                    nuevos_dominios[f].remove(col)
                diag1 = col + (f - fila)
                diag2 = col - (f - fila)
                nuevos_dominios[f] = [c for c in nuevos_dominios[f]
                                      if c not in (diag1, diag2)]
                if not nuevos_dominios[f]:
                    consistente = False
                    break
            if consistente and fc(asignacion, nuevos_dominios, fila + 1):
                return True
            asignacion[fila] = -1
        return False

    dominios_iniciales = [list(range(N)) for _ in range(N)]
    fc([-1] * N, dominios_iniciales, 0)
    return soluciones, nodos
