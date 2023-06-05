import matplotlib.pyplot as plt
import pandas as pd

# Wczytanie danych z pliku CSV
data = pd.read_csv('results.csv', delimiter=';')

grouped_data = data.groupby('threads_per_block')

color_palette = plt.cm.get_cmap('tab20')  # Wybór palety kolorów
for i, (group_name, group_data) in enumerate(grouped_data):
    mean_time = group_data.groupby('vector_size')['time'].mean()
    plt.plot(mean_time.index, mean_time.values, linestyle='dashed', marker='o', label=str(group_name), color=color_palette(i))

custom_xticks = [3355443, 3355443 * 2, 3355443 * 3, 3355443 * 4, 3355443 * 5]
custom_xtick_labels = [str(x) for x in custom_xticks]
plt.xticks(custom_xticks, custom_xtick_labels)
plt.grid(True)

plt.legend(title='Threads per block')
plt.title("CUDA Add vector operation times to vector length")
plt.xlabel('Vector elements')
plt.ylabel('time [ms]')
plt.show()