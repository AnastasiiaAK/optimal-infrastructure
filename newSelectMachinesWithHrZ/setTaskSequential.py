import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


# firstVariant - sequential task
# without possibility of paralleling each task


def set_task(number_of_task):
    g = nx.DiGraph()
    nodes = list(range(number_of_task))
    edges = list(map(lambda nod: nodes[nod:(nod + 2)], nodes))[:-1]
    g.add_edges_from(edges)
    assert (nx.is_directed_acyclic_graph(g) == True)  # check if graph is DAG

    # nx.draw(g, with_labels=True)  # draw
    # plt.title("Sequential task")
    # plt.show()
    return g


# working time of task on CPU
"""
CPU
Task 1 0.11952686309814453
Task 2 0.38246989250183105
Task 3 0.0005393028259277344
Task 4 1.6666145324707031
Task 5 1451.2022745609283
Task 6 0.67854
Task 7 0.4834657
"""

# set number of task
number_of_task = 7

# set graph of task (sequential)
taskGraph = set_task(number_of_task)

data = [[0, 0, round(0.11952686309814453, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [1, 1, round(0.38246989250183105, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [2, 2, round(0.0005393028259277344, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [3, 3, round(1.6666145324707031, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [4, 4, round(1451.2022745609283, 2), 0, 0, 1, None, None, None, None, None, "No"],
        [5, 5, round(0.67854, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [6, 6, round(0.4834657, 2), 0, 0, 0, None, None, None, None, None, "No"]]

descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask", "incomingMemory",
                                                 "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                                 "startTime", "endTime", "executingTime", "transferPrice", "done"])
