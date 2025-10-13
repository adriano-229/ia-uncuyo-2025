import csv
import time

from backtracking import backtracking_n_queens
from forward_checking import forward_checking_n_queens
from metrics import calcular_metricas


def medir(algoritmo, N, intentos=30):
    resultados = []
    for seed in range(intentos):
        # seed controla la aleatoriedad dentro del algoritmo
        t0 = time.time()
        soluciones, nodos = algoritmo(N, seed)  # <-- pasar seed
        t1 = time.time()
        resultados.append({
            "algoritmo": algoritmo.__name__,
            "N": N,
            "semilla": seed,
            "tiempo": t1 - t0,
            "nodos": nodos,
            "exito": len(soluciones) > 0
        })
    return resultados


def ejecutar_experimento():
    Ns = [4, 8, 10]
    resultados_totales = []

    for N in Ns:
        resultados_totales += medir(backtracking_n_queens, N)
        resultados_totales += medir(forward_checking_n_queens, N)

    with open("tp5-Nreinas.csv", "w", newline="") as f:
        campos = ["algoritmo", "N", "semilla", "tiempo", "nodos", "exito"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados_totales)

    # Imprimir resumen estadístico
    resumen = calcular_metricas(resultados_totales)
    for r in resumen:
        print(f"N={r['N']:>2} | {r['algoritmo']:<25} "
              f"| Éxito={r['porc_exito']:5.1f}% "
              f"| Tiempo={r['prom_tiempo']:.4f}s±{r['desv_tiempo']:.4f} "
              f"| Nodos={r['prom_nodos']:.1f}±{r['desv_nodos']:.1f}")


if __name__ == "__main__":
    ejecutar_experimento()
