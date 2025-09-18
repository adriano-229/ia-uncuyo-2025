import os

from experiments import run_experiments
from plotting import plot_boxplots
from plotting import plot_example_histories

OUTPUT_ROOT = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(OUTPUT_ROOT, "tp4-Nreinas.csv")
REPORT_PATH = os.path.join(OUTPUT_ROOT, "tp4-reporte.md")
IMAGES_DIR = os.path.join(OUTPUT_ROOT, "images")

SIZES = [4, 8, 10, 12, 15]
ALGOS = ["random", "HC", "SA", "GA"]
N_SEEDS = 30
MAX_STATES = 10000

os.makedirs(IMAGES_DIR, exist_ok=True)


def main():
    df = run_experiments(SIZES, ALGOS, N_SEEDS, MAX_STATES, CSV_PATH)
    plot_boxplots(df, SIZES, IMAGES_DIR)
    plot_example_histories(SIZES[len(SIZES) - 1], seed=0, images_dir=IMAGES_DIR)
    print("Experiments complete. See:", CSV_PATH, REPORT_PATH, IMAGES_DIR)


if __name__ == "__main__":
    main()
