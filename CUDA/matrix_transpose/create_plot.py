import matplotlib.pyplot as plt
import pandas as pd

# Wczytanie danych z pliku CSV
data = pd.read_csv('results.csv', delimiter=';')

grouped_data = data.groupby(['grid_size', 'type'])

color_palette = plt.cm.get_cmap('tab20')  # Wybór palety kolorów
for i, ((grid_size, type), group_data) in enumerate(grouped_data):
    mean_time = group_data.groupby('block_size')['time'].mean()
    plt.plot(mean_time.index, mean_time.values, linestyle='dashed', marker='o', label=f'{grid_size} ({type})', color=color_palette(i))

custom_xticks = [64, 128, 256, 512, 1024]
custom_xtick_labels = [str(x) for x in custom_xticks]
plt.xticks(custom_xticks, custom_xtick_labels)
plt.grid(True)

plt.legend(title='Grid size (Type)')
plt.title("CUDA Transpose Matrix operation times to block size")
plt.xlabel('Block size')
plt.ylabel('time [ms]')
plt.show()