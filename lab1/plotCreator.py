import pandas as pd
from matplotlib import pyplot as plt

node1 = pd.read_csv("node1_results.csv", sep=';', usecols=["bytes", "throughput"])
node2 = pd.read_csv("node2_results.csv", sep=';', usecols=["bytes", "throughput"])
node1_sync = pd.read_csv("node1_sync_results.csv", sep=';', usecols=["bytes", "throughput"])
node2_sync = pd.read_csv("node2_sync_results.csv", sep=';', usecols=["bytes", "throughput"])

plt.title('2 nodes communication')
plt.xlabel('message length [B]')
plt.ylabel('throughput [Mbit/s]')
plt.grid(color='grey', linestyle='-', linewidth=1)

# plt.plot(node1.bytes, node1.throughput, label="MPI_Send")
# plt.plot(node1_sync.bytes, node1_sync.throughput, label="MPI_Ssend", color='orange')

plt.plot(node2.bytes, node2.throughput, label="MPI_Send")
plt.plot(node2_sync.bytes, node2_sync.throughput, label="MPI_Ssend", color='orange')
plt.show()