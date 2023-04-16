import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


LEGEND = ['Losowanie', 'Rozdzielanie do kubełków',
          'Sortowanie', 'Scalanie tablicy', 'Sumarycznie']

SYNC_FILE_PATH = 'sync.csv'
ASYNC_FILE_PATH = 'async.csv'


def draw_chart_1():
    df = pd.read_csv(SYNC_FILE_PATH)

    grouped_df = df.groupby('bsize')['total'].mean().reset_index()

    x = grouped_df['bsize']
    y = grouped_df['total']
    plt.scatter(x, y)
    plt.xlabel('Rozmiar kubełka')
    plt.ylabel('Całkowity czas wykonania [s]')
    plt.title('Zależność czasu wykonania algorytmu sekwencyjnego od ilości kubełków')
    plt.legend(['Rozwiązanie synchroniczne'])
    plt.grid(True)


def draw_chart_2():
    df = pd.read_csv(ASYNC_FILE_PATH)

    pivoted_df = pd.pivot_table(df, values=[
                                'total', 'draw', 'scatter', 'sort', 'gather'], index=['nthreads'], aggfunc='mean')

    pivoted_df = pivoted_df.iloc[0] / pivoted_df

    _, ax = plt.subplots()
    for name, values in pivoted_df.iteritems():
        ax.plot(values.index, values, label=name,
                marker='o', linestyle='--')

    plt.xlabel('Ilość wątków')
    plt.ylabel('Przyspieszenie')
    plt.title('Przyspieszenie w zależności od ilości wątków')
    plt.legend(LEGEND)
    plt.grid(True)

    nthreads_values = df['nthreads']
    ax.set_xticks(nthreads_values)


def draw_chart_3():
    bar_width = 0.3
    data = pd.read_csv(ASYNC_FILE_PATH)
    data = data.drop(['sid', 'arrsize', 'bsize'], axis=1)

    data = data.groupby('nthreads').mean()

    r1 = np.arange(len(data['total']))
    r1 = [x + bar_width for x in r1]

    ax = data[['draw', 'scatter', 'sort', 'gather']].plot(
        kind='bar', stacked=True, width=bar_width)

    ax.bar(r1, data['total'], color='gray',
           width=bar_width, label='total')

    ax.set_xticklabels(data.index, rotation=0)

    ax.legend(LEGEND)
    ax.set_xlabel("Ilość wątków")
    ax.set_ylabel("Czas wykonania [s]")
    ax.set_title("Czas wykonania w zależności od ilości wątków")
    ax.grid(True)


draw_chart_1()
# draw_chart_2()
# draw_chart_3()
plt.show()
