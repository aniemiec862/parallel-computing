import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


LEGEND = ['Generating', 'Scattering',
          'Sorting', 'Merging', 'Total']

SYNC_FILE_PATH = 'sync.csv'
ASYNC_FILE_PATH = 'async_500.csv'


def draw_chart_1():
    df = pd.read_csv(SYNC_FILE_PATH)

    grouped_df = df.groupby('bsize')['total'].mean().reset_index()
    grouped_df['total'] = grouped_df['total'] / 1000000

    x = grouped_df['bsize']
    y = grouped_df['total']
    plt.scatter(x, y)
    plt.xlabel('Average bucket size')
    plt.ylabel('Execution time [s]')
    plt.title('Execution time per average bucket size')
    plt.grid(True)


def draw_chart_2():
    df = pd.read_csv(ASYNC_FILE_PATH)

    pivoted_df = pd.pivot_table(df, values=[
                                'total', 'draw', 'scatter', 'sort', 'gather'], index=['nthreads'], aggfunc='mean')

#TODO use result from sync instead
    pivoted_df = pivoted_df.iloc[0] / pivoted_df

    _, ax = plt.subplots()
    for name, values in pivoted_df.iteritems():
        x = [i for i in values.index if i % 4 == 1]
        y = [values[i] for i in x]
        if name == 'total':
            ax.plot(x, y, label=name, color='pink', marker='^', linestyle=':')
        else:
            ax.plot(x, y, label=name, marker='^', linestyle=':')

    plt.xlabel('Number of threads')
    plt.ylabel('Speedup')
    plt.title('Speedup per number of threads')
    plt.legend(LEGEND)
    plt.grid(True)

    nthreads_values = list(df['nthreads'].unique())

    xticks = []
    for i in range(0, len(nthreads_values), 4):
        xticks.append(nthreads_values[i])

    ax.set_xticks(xticks)


def draw_chart_3():
    bar_width = 0.3
    data = pd.read_csv(ASYNC_FILE_PATH)
    data = data.drop(['sid', 'arrsize', 'bsize'], axis=1)

    data = data.groupby('nthreads').mean()

    r1 = np.arange(len(data['total']))
    r1 = [x + bar_width for x in r1]

    data['total'] = data['total'] / 1000000
    data['draw'] = data['draw'] / 1000000
    data['scatter'] = data['scatter'] / 1000000
    data['sort'] = data['sort'] / 1000000
    data['gather'] = data['gather'] / 1000000

    ax = data[['draw', 'scatter', 'sort', 'gather']].plot(
        kind='bar', stacked=True, width=bar_width)

    ax.bar(r1, data['total'], color='gray',
           width=bar_width, label='total')

    ax.set_xticklabels(data.index, rotation=0)

    ax.legend(LEGEND)
    ax.set_xlabel("Number of threads")
    ax.set_ylabel("Execution time [s]")
    ax.set_title("Execution time per number of threads")
    ax.set_axisbelow(True)
    ax.grid(True)


# draw_chart_1()
draw_chart_2()
# draw_chart_3()
plt.show()
