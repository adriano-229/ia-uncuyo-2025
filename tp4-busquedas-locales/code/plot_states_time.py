import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Resolve base directory as parent of this script (code/)
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

# Load data (CSV en el directorio padre)
csv_path = BASE_DIR / 'tp4-Nreinas.csv'
if not csv_path.exists():
    raise FileNotFoundError(f'No se encontró el CSV en {csv_path}')

df = pd.read_csv(csv_path)

# Ensure output directory exists (guardar dentro de tp4-busquedas-locales/images)
img_dir = BASE_DIR / 'images'
img_dir.mkdir(parents=True, exist_ok=True)

# Metrics to plot (boxplots por N y algoritmo)
metrics = ['states', 'time']

for metric in metrics:
    for n in sorted(df['size'].unique()):
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='algorithm_name', y=metric, data=df[df['size'] == n])
        plt.title(f'Boxplot {metric} N={n}')
        plt.xlabel('Algoritmo')
        plt.ylabel(metric.capitalize())
        plt.tight_layout()
        fname = f'boxplot_{metric}_N{n}.png'
        plt.savefig(img_dir / fname)
        plt.close()

# --- NUEVOS GRAFICOS AGREGADOS: promedio vs N ---
summary = df.groupby(['algorithm_name', 'size']).agg(
    mean_time=('time', 'mean'), std_time=('time', 'std'),
    mean_states=('states', 'mean'), std_states=('states', 'std'),
    solved_rate=('H', lambda s: (s == 0).mean())
).reset_index()

algorithm_order = ['HC', 'SA', 'GA', 'random']
colors = {
    'HC': '#1f77b4',
    'SA': '#ff7f0e',
    'GA': '#2ca02c',
    'random': '#d62728'
}

# Tiempo promedio vs N
plt.figure(figsize=(9, 6))
for algo in algorithm_order:
    sub = summary[summary['algorithm_name'] == algo].sort_values('size')
    if sub.empty:
        continue
    plt.errorbar(sub['size'], sub['mean_time'], yerr=sub['std_time'], label=algo,
                 marker='o', capsize=4, color=colors.get(algo))
plt.title('Tiempo promedio vs N (30 semillas)')
plt.xlabel('N')
plt.ylabel('Tiempo (s)')
plt.grid(alpha=0.3)
plt.legend(title='Algoritmo')
plt.tight_layout()
plt.savefig(img_dir / 'time_vs_N.png')
plt.close()

# Estados promedio vs N (escala lineal)
plt.figure(figsize=(9, 6))
for algo in algorithm_order:
    sub = summary[summary['algorithm_name'] == algo].sort_values('size')
    if sub.empty:
        continue
    plt.errorbar(sub['size'], sub['mean_states'], yerr=sub['std_states'], label=algo,
                 marker='o', capsize=4, color=colors.get(algo))
plt.title('Estados explorados promedio vs N (30 semillas)')
plt.xlabel('N')
plt.ylabel('Estados')
plt.grid(alpha=0.3)
plt.legend(title='Algoritmo')
plt.tight_layout()
plt.savefig(img_dir / 'states_vs_N.png')
plt.close()

# Estados promedio vs N (escala log) para distinguir mejor curvas pequeñas frente a random/GA
plt.figure(figsize=(9, 6))
for algo in algorithm_order:
    sub = summary[summary['algorithm_name'] == algo].sort_values('size')
    if sub.empty:
        continue
    plt.errorbar(sub['size'], sub['mean_states'], yerr=sub['std_states'], label=algo,
                 marker='o', capsize=4, color=colors.get(algo))
plt.title('Estados explorados promedio vs N (escala log)')
plt.xlabel('N')
plt.ylabel('Estados (log)')
plt.yscale('log')
plt.grid(alpha=0.3, which='both')
plt.legend(title='Algoritmo')
plt.tight_layout()
plt.savefig(img_dir / 'states_vs_N_log.png')
plt.close()

summary.to_csv(os.path.join(img_dir, 'summary_time_states.csv'), index=False)
