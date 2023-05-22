import pandas as pd
import matplotlib.pyplot as plt

def draw_time_plot(filename):
    data = pd.read_csv(filename, sep=";")

    ncolumn = 'nCores'
    confId = 'confId'
    dataSize = 'dataSize'
    timecolumn = 'time'

    averaged_data = data.groupby([ncolumn, confId, dataSize]).mean().reset_index()

    plt.figure(figsize=(10, 6))
    for key, grp in averaged_data.groupby([ncolumn, confId]):
        plt.plot(grp[dataSize], grp[timecolumn], linestyle=':', marker='o', label=f"confId={key[1]}, nCores={key[0]}")
    plt.xlabel('Data size[GB]')
    plt.ylabel('Time [s]')
    plt.title('Time to data size')
    plt.xticks(range(11))
    plt.yticks(range(0, 1100, 100))
    plt.legend()
    plt.grid(True)
    plt.show()

def draw_speedup_plot(filename):
    data = pd.read_csv(filename, sep=";")

    ncolumn = 'nCores'
    confId = 'confId'
    dataSize = 'dataSize'
    timecolumn = 'time'


    averaged_data = data.groupby([ncolumn, confId, dataSize]).mean().reset_index()

    reference_values = {
        1: 51.703,
        5: 253.662,
        10: 523.132
    }

    averaged_data['speedup'] = averaged_data.apply(
        lambda row: reference_values.get(row[dataSize], 1) / row[timecolumn], axis=1)

    plt.figure(figsize=(10, 6))
    for key, grp in averaged_data.groupby([ncolumn, confId]):
        plt.plot(grp[dataSize], grp['speedup'], marker='o', label=f"confId={key[1]}, nCores={key[0]}")
    plt.xlabel('Data size[GB]')
    plt.ylabel('Speedup')
    plt.title('Speedup to data size')
    plt.legend()
    plt.xticks(range(11))
    plt.grid(True)
    plt.show()


# draw_time_plot("results.csv")
draw_speedup_plot("results.csv")
