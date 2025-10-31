from GraphTsetlinMachine.graphs import Graphs
import numpy as np
from scipy.sparse import csr_matrix
from GraphTsetlinMachine.tm import MultiClassGraphTsetlinMachine
from time import time
import argparse
from skimage.util import view_as_windows
from numba import jit
import random


number_of_examples = 10000

# === Create Training Graph ===
graphs_train = Graphs(
    number_of_examples,
    symbols = ['A', 'B'],
    hypervector_size = 32,
    hypervector_bits = 2
)

for graph_id in range(number_of_examples):
    graphs_train.set_number_of_graph_nodes(graph_id, 2)

graphs_train.prepare_node_configuration()

for graph_id in range(number_of_examples):
   number_of_outgoing_edges = 1
   graphs_train.add_graph_node(graph_id, 'Node 1', number_of_outgoing_edges)
   graphs_train.add_graph_node(graph_id, 'Node 2', number_of_outgoing_edges)

graphs_train.prepare_edge_configuration()

for graph_id in range(number_of_examples):
    edge_type = "Plain"
    graphs_train.add_graph_node_edge(graph_id, 'Node 1', 'Node 2', edge_type)
    graphs_train.add_graph_node_edge(graph_id, 'Node 2', 'Node 1', edge_type)


# === Assign Properties and Labels ===
Y_train = np.empty(number_of_examples, dtype=np.uint32)
for graph_id in range(number_of_examples):
    x1 = random.choice(['A', 'B'])
    x2 = random.choice(['A', 'B'])

    graphs_train.add_graph_node_property(graph_id, 'Node 1', x1)
    graphs_train.add_graph_node_property(graph_id, 'Node 2', x2)


    if x1 == x2:
        Y_train[graph_id] = 0
    else:
        Y_train[graph_id] = 1

    # Add 1% label noise
    if np.random.rand() <= 0.01:
        Y_train[graph_id] = 1 - Y_train[graph_id]


graphs_train.encode()

print("\n\nCreating testing data\n")

# === Create Test Graphs ===
graphs_test = Graphs(number_of_examples, init_with=graphs_train)

# 1 - Define number of nodes
for graph_id in range(number_of_examples):
    graphs_test.set_number_of_graph_nodes(graph_id, 2)

# 2 - Prepare node configuration
graphs_test.prepare_edge_configuration()

# 3 - Add nodes
for graph_id in range(number_of_examples):
    graphs_test.add_graph_node(graph_id, 'Node 1', 1)
    graphs_test.add_graph_node(graph_id, 'Node 2', 1)

# 4 - Prepare edge configuration
graphs_test.prepare_edge_configuration()

# 5 - Add edges
for graph_id

Y_test = np.empty(number_of_examples, dtype=np.uint32)
for graph_id in range(number_of_examples):
    x1 = random.choice(['A', 'B'])
    x2 = random.choice(['A', 'B'])

    graphs_test.add_graph_node_property(graph_id, 'Node 1', x1)
    graphs_test.add_graph_node_property(graph_id, 'Node 2', x2)

    Y_test[graph_id] = 0 if x1 == x2 else 1


graphs_test.encode()

# === Graph Test Summary
print("="*30)
print("Graph Test Summary")
print("="*30)
print(f"{'Hypervectors:':<15}")
print(graphs_test.hypervectors)
print("\n" + f"{'Edge Type ID:':<15}")
print(graphs_test.edge_type_id)
print("="*30 + "\n")


# === Train Graphs Tsetlin Machine ===
tm = MultiClassGraphTsetlinMachine(number_of_clauses=1000, T=500, s=10.0)

print(f"Initializing and training Graph Tsetlin Machine...\n")
for epoch in range(5):
    start = time()
    tm.fit(graphs_train, Y_train, epochs=1)
    result = 100 * (tm.predict(graphs_test) == Y_test).mean()
    print(f"{epoch} {result:.2f}% Accuracy ({time() - start:.2f}s)")

print(f"\nDone!\n")


exit("")

# === Create Test Graphs ===
graphs_test = Graphs(10000, init_with=graphs_train)

# 1️⃣ Define number of nodes
for graph_id in range(10000):
    graphs_test.set_number_of_graph_nodes(graph_id, 2)

# 2️⃣ Prepare node configuration
graphs_test.prepare_node_configuration()

# 3️⃣ Add nodes
for graph_id in range(10000):
    graphs_test.add_graph_node(graph_id, 'Node 1', 1)
    graphs_test.add_graph_node(graph_id, 'Node 2', 1)

# 4️⃣ Prepare edge configuration
graphs_test.prepare_edge_configuration()

# 5️⃣ Add edges
for graph_id in range(10000):
    edge_type = "Plain"
    graphs_test.add_graph_node_edge(graph_id, 'Node 1', 'Node 2', edge_type)
    graphs_test.add_graph_node_edge(graph_id, 'Node 2', 'Node 1', edge_type)

# 6️⃣ Add node properties and labels
Y_test = np.empty(10000, dtype=np.uint32)
for graph_id in range(10000):
    x1 = random.choice(['A', 'B'])
    x2 = random.choice(['A', 'B'])

    graphs_test.add_graph_node_property(graph_id, 'Node 1', x1)
    graphs_test.add_graph_node_property(graph_id, 'Node 2', x2)

    Y_test[graph_id] = 0 if x1 == x2 else 1

graphs_test.encode()
