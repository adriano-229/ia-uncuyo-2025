import matplotlib.pyplot as plt
import pandas as pd


def generar_boxplots(csv_file="tp5-Nreinas.csv", carpeta="../images"):
    data = pd.read_csv(csv_file)

    for N in sorted(data["N"].unique()):
        subset = data[data["N"] == N]

        plt.figure()
        subset.boxplot(column="tiempo", by="algoritmo")
        plt.title(f"Tiempos para N={N}")
        plt.suptitle("")
        plt.ylabel("segundos")
        plt.savefig(f"{carpeta}/boxplot_tiempo_{N}.png", bbox_inches="tight")

        plt.figure()
        subset.boxplot(column="nodos", by="algoritmo")
        plt.title(f"Nodos explorados para N={N}")
        plt.suptitle("")
        plt.ylabel("cantidad de nodos")
        plt.savefig(f"{carpeta}/boxplot_nodos_{N}.png", bbox_inches="tight")

    print("Boxplots generados en carpeta:", carpeta)


if __name__ == "__main__":
    generar_boxplots()
