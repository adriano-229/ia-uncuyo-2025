import statistics


def calcular_metricas(resultados):
    """Dado un conjunto de dicts con claves:
       algoritmo, N, tiempo, nodos, exito.
       Devuelve un resumen estadístico por (algoritmo, N)."""
    resumen = {}
    for r in resultados:
        key = (r["algoritmo"], r["N"])
        if key not in resumen:
            resumen[key] = {"tiempos": [], "nodos": [], "exitos": 0}
        resumen[key]["tiempos"].append(r["tiempo"])
        resumen[key]["nodos"].append(r["nodos"])
        resumen[key]["exitos"] += int(r["exito"])

    salida = []
    for (alg, N), data in resumen.items():
        n = len(data["tiempos"])
        salida.append({
            "algoritmo": alg,
            "N": N,
            "prom_tiempo": statistics.mean(data["tiempos"]),
            "desv_tiempo": statistics.pstdev(data["tiempos"]),
            "prom_nodos": statistics.mean(data["nodos"]),
            "desv_nodos": statistics.pstdev(data["nodos"]),
            "porc_exito": 100 * data["exitos"] / n
        })
    return salida
