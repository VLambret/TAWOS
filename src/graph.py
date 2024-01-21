import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from time_series.cumulative_time_series import CumulativeTimeSeries


def save_as_graph(project, title: str, all_data_to_plot: dict[str, CumulativeTimeSeries]):
    figure = Figure(figsize=(8, 6))

    filename = project.folder / (title.replace(' ', '_') + ".png")

    figure_axis = figure.add_subplot()
    figure.suptitle(f"{project.name} - {title}")
    figure_axis.set_xlabel('Date')
    figure_axis.set_ylabel('# of Completed issues')

    for label, data in all_data_to_plot.items():
        estimates_dates = data.get_dates()
        estimates_values = data.get_values()
        figure_axis.plot(estimates_dates, estimates_values, label=label)

    figure_axis.legend()

    figure.savefig(filename, dpi=300)
