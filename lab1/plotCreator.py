import pandas as pd
from matplotlib import pyplot as plt

node1 = pd.read_csv("n_node1_results.csv", sep=';', usecols=["b", "t"])
node2 = pd.read_csv("n_node2_results.csv", sep=';', usecols=["b", "t"])
node1_sync = pd.read_csv("n_node1_sync_results.csv", sep=';', usecols=["b", "t"])
node2_sync = pd.read_csv("n_node2_sync_results.csv", sep=';', usecols=["b", "t"])

plt.title('Throughput for 2 nodes communication')
plt.xlabel('Message length [B]')
plt.ylabel('Throughput [Mbit/s]')
plt.grid(color='grey', linestyle='-', linewidth=1)

# plt.plot(node1.b, node1.t, label="MPI_Send")
# plt.plot(node1_sync.b, node1_sync.t, label="MPI_Ssend", color='orange')

plt.plot(node2.b, node2.t, label="MPI_Send")
plt.plot(node2_sync.b, node2_sync.t, label="MPI_Ssend", color='orange')
plt.legend()
plt.show()