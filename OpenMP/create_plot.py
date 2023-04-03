filenames = ['static.csv', 'dynamic.csv', 'guided.csv', 'runtime.csv', 'auto.csv']

import pandas as pd
import matplotlib.pyplot as plt

for filename in filenames:
    data = pd.read_csv(filename, header=None, sep=';')

    groups = data.groupby(data.iloc[:, 2])

    time_fig, ax1 = plt.subplots()
    time_fig.set_size_inches(8, 6)

    for group_name, group_data in groups:
        ax1.plot(group_data.iloc[:, 0], group_data.iloc[:, 1], linestyle='--', marker='D', label=f'array size: {group_name}')

    ax1.set_xlabel('Number of threads')
    ax1.set_ylabel('Execution time [s]')
    ax1.set_title(f'Execution time - schedule {filename[:-4]}')
    ax1.legend()
    ax1.grid(True)

    ax1.set_xticks(data.iloc[:, 0].unique())

    time_fig.savefig(f'time_chart_{filename[:-4]}.png', dpi=300)

    speedup_fig, ax2 = plt.subplots()
    speedup_fig.set_size_inches(8, 6)

    for group_name, group_data in groups:
        speedup = group_data.iloc[0, 1] / group_data.iloc[:, 1]
        ax2.plot(group_data.iloc[:, 0], speedup, linestyle='--', marker='D', label=f'array_chart: {group_name}')

    ax2.set_xlabel('Number of threads')
    ax2.set_ylabel('Speedup')
    ax2.set_title(f'Speedup - schedule {filename[:-4]}')
    ax2.legend()
    ax2.grid(True)

    ax2.set_xticks(data.iloc[:, 0].unique())

    speedup_fig.savefig(f'speedup_chart_{filename[:-4]}.png', dpi=300)