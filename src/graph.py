import re

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from time_series.cumulative_time_series import CumulativeTimeSeries


def save_as_graph(project, title: str, x_label, y_label, all_data_to_plot: dict[str, CumulativeTimeSeries]):
    figure = Figure(figsize=(8, 6))

    filename = project.folder / (_sanitize(title) + ".png")

    figure_axis = figure.add_subplot()
    figure.suptitle(f"{project.name} - {title}")
    figure_axis.set_xlabel(x_label)
    figure_axis.set_ylabel(y_label)

    for label, data in all_data_to_plot.items():
        # TODO: make all data to plot a dict and not a CumulativeTimeSeries
        estimates_dates = data.get_dates()
        estimates_values = data.get_values()
        figure_axis.plot(estimates_dates, estimates_values, label=label)

    figure_axis.legend()

    figure.savefig(filename, dpi=300)


def _sanitize(title: str) -> str:
    return re.sub(r'\W+', '_',title).strip('_')