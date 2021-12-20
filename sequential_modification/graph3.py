
descendant_parent_pairs = [
    ('Alexei', 'Peter_I'),
    ('Anna', 'Peter_I'),
    ('Elizabeth', 'Peter_I'),
    ('Peter_II', 'Alexei'),
    ('Peter_III', 'Anna'),
    ('Paul_I', 'Peter_III'),
    ('Alexander_I', 'Paul_I'),
    ('Nicholaus_I', 'Paul_I'),
]



import sys

sys.setrecursionlimit(100000)

class GenealogicalTreeNode:
    def __init__(self, name):
        self.name = name
        self.parent = None

nodes = {}
for (descendant, parent) in descendant_parent_pairs:
    # из каждого имени создаем дерево
    if parent not in nodes:
        nodes[parent] = GenealogicalTreeNode(parent)
    if descendant not in nodes:
        nodes[descendant] = GenealogicalTreeNode(descendant)

    # добавляем для каждого имени его потомка
    nodes[descendant].parent = (nodes[parent])


name1, name2 = ("Alexander_I", "Nicholaus_I")


res1 = set()  # Set to keep track of visited nodes of graph.

graph = nodes["Alexander_I"]


def dfs(visited, graph, name1):  #function for dfs
    print(name1)
    if graph.parent != None:
        visited.add(name1)
        dfs(visited, graph.parent, graph.parent.name)


dfs(res1, graph, name1)

