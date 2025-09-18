import matplotlib.pyplot as plt
import pandas as pd


def plot_boxplots(input_file="results.csv"):
    df = pd.read_csv(input_file)
    metrics = ["states_n", "actions_count", "actions_cost", "time"]

    for metric in metrics:
        plt.figure(figsize=(10, 6))

        # Copy data to avoid modifying the original DataFrame
        df_metric = df.copy()

        # Replace zeros with small value for log scale compatibility
        df_metric[metric] = df_metric[metric].replace(0, 0.001)

        # Create boxplot grouped by algorithm and scenario
        ax = df_metric.boxplot(column=metric, by=["algorithm_name", "scenario"], grid=False)

        # Calculate group statistics
        grouped = df_metric.groupby(["algorithm_name", "scenario"])[metric]
        means = grouped.mean()
        stds = grouped.std()

        # Overlay means as small red dots
        positions = range(1, len(means) + 1)
        plt.scatter(positions, means, color="red", marker="o", s=2, alpha=0.7, label="Mean")
        plt.plot([], [], color="blue", marker="o", linestyle="", label="Standard Deviation")

        # Add std deviation text above whiskers
        for pos, (group, mean) in enumerate(means.items(), start=1):
            std = stds[group]
            whisker_vals = []
            for line in ax.lines:
                xdata = line.get_xdata()
                ydata = line.get_ydata()
                if len(xdata) > 0 and xdata[0] == pos:
                    whisker_vals.extend(ydata)
            top_whisker = max(whisker_vals) if whisker_vals else mean
            plt.text(pos, top_whisker * 1.15, f"{std:.1f}", ha="center", va="bottom", fontsize=5, color="blue",
                     alpha=0.7)

        # Titles and labels
        plt.title(f"Distribution of {metric} by Algorithm and Scenario")
        plt.suptitle("")  # remove automatic grouped title
        plt.xlabel("Algorithm & Scenario")
        plt.ylabel(metric)
        plt.xticks(rotation=45)

        # Check if log scale is appropriate
        min_val = df_metric[metric].min()
        max_val = df_metric[metric].max()
        if min_val > 0 and max_val / min_val > 1000:
            plt.yscale("log")
            plt.ylabel(f"{metric} (log scale)")

        plt.legend()
        plt.tight_layout()
        plt.savefig(f"../images/{metric}_boxplot.png", dpi=300, bbox_inches='tight')
        plt.close()

    print("Enhanced boxplots saved in ../images/")


if __name__ == "__main__":
    plot_boxplots()
