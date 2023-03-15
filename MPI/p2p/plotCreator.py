import pandas as pd
from matplotlib import pyplot as plt

node1 = pd.read_csv("node1_results.csv", sep=';', usecols=["b", "t"])
node2 = pd.read_csv("node2_results.csv", sep=';', usecols=["b", "t"])
node1_sync = pd.read_csv("node1_sync_results.csv", sep=';', usecols=["b", "t"])
node2_sync = pd.read_csv("node2_sync_results.csv", sep=';', usecols=["b", "t"])

plt.title('Throughput for 1 node communication')
plt.xlabel('Message length [B]')
plt.ylabel('Throughput [Mbit/s]')
plt.grid(color='grey', linestyle='-', linewidth=1)

plt.plot(node1.b, node1.t, label="MPI_Send")
# plt.scatter(node1_sync.b, node1_sync.t, label="MPI_Ssend", color='orange')

# plt.scatter(node2.b, node2.t, label="MPI_Send")
# plt.scatter(node2_sync.b, node2_sync.t, label="MPI_Ssend", color='orange')

plt.legend()
plt.show()
