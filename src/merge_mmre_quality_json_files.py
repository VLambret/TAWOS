import json
import sys
from typing import List

from matplotlib import pyplot as plt


def aggregate_data(file_paths):
    aggregated_data = {}

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            json_content = json.load(file)

        if isinstance(json_content, dict):
            aggregated_data.update(json_content)

    return aggregated_data

def plot_boxplots(aggregated_data, output_file) -> None:
    periods = list(next(iter(aggregated_data.values())).keys())

    group_by_period: dict[int, List[float]] = {
        k: []
        for k in periods
    }

    for project in aggregated_data.values():
        for period, value in project.items():
            group_by_period[period].append(value)

    data_for_boxplot = list(group_by_period.values())

    plt.boxplot(data_for_boxplot, labels=periods)
    plt.xlabel('Period')
    plt.ylabel('Metric Value')
    plt.title('Boxplots for Each Period and Metric')

    plt.savefig(output_file, dpi=300)


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py file1.json file2.json ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    aggregated_data_result = aggregate_data(file_paths)
    plot_boxplots(aggregated_data_result, "all_mmre_quality_per_period.png")


if __name__ == "__main__":
    main()
