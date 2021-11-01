# create the possibility of ditribution of each tasks in workflow
import random
import networkx as nx
from collections.abc import Iterable
import matplotlib.pyplot as plt


def posibilityOfDistributionOfTasks(maxNumberOfTasks):
    maxNumberOfTasks = 16
    dPossibilityOfDistributionOfEachTask = {}
    for i in range(maxNumberOfTasks):
        a = random.random()
        if (a-0.5) < 0:
            dPossibilityOfDistributionOfEachTask[i+1] = 0
        else:
            dPossibilityOfDistributionOfEachTask[i+1] = (a - 0.5)
    return dPossibilityOfDistributionOfEachTask


# flatten Graph
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


# generate task
def generateTask(maxNumberOfTasks):
    listOfNodes = list(range(1, maxNumberOfTasks + 1))
    listOfEdges = []
    adjancyList = {}
    adjancyList[listOfNodes[-1]] = []
    for i in listOfNodes[:-1]:
        a = random.random()
        # numbersInLayer = round(a/i * maxNumberOfTasks)
        numbersInLayer = round(posibilityOfDistributionOfTasks(maxNumberOfTasks)[i] * maxNumberOfTasks)
        maxNumber = i + numbersInLayer
        if maxNumber > maxNumberOfTasks:
            maxNumber = maxNumberOfTasks
        potentialChildNodes = list(range(i + 2, maxNumber))

        childNodes = potentialChildNodes

        valInLists = list(flatten(list(adjancyList.values())))

        if (i + 1) not in valInLists:
            listOfEdges.append([i, i + 1])
            potentialChildNodes.append(i + 1)

        adjancyList[i] = childNodes
        # adjancyList[i].append(i+1)
        # listOfEdges.append([i, i+1])
        for j in childNodes:
            listOfEdges.append([i, j])

    G = nx.DiGraph()
    G.add_edges_from(listOfEdges)

    for node in list(G.nodes()):
        if not nx.has_path(G, node, maxNumberOfTasks):
            adjancyList[node].append(maxNumberOfTasks)
            listOfEdges.append([node, maxNumberOfTasks])

    # print(adjancyList)

    G.add_edges_from(listOfEdges)
    return G


numbersOfTasks = 16
G = generateTask(numbersOfTasks)
print("This graph is DAG?",nx.is_directed_acyclic_graph(G))  # check if graph is DAG
nx.draw(G, with_labels=True)# draw
plt.show()

# numbers Of Nodes and edges
numbersOfNodes = len(G.nodes())
numbersOfEdges = len(G.edges())
print("numbersOfNodes:", numbersOfNodes, "numbersOfEdges:", numbersOfEdges)

