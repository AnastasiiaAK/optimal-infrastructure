p = [["Alexei", "Peter_I"], ["Anna" ,"Peter_I"],["Elizabeth" ,"Peter_I"], ["Peter_II", "Alexei"], ["Peter_III",  "Anna"], ["Paul_I", "Peter_III"], ["Alexander_I" ,"Paul_I"], ["Nicholaus_I", "Paul_I"], ["Anna", "Nicholaus_I"]]

import sys

sys.setrecursionlimit(100000)

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

# найдем имя в ноде, где левел = 0
n = int(input())
descendant_parent_pairs = []
for _ in range(n-1):
  child, parent = map(str, input().split())
  descendant_parent_pairs.append((child, parent))



query = []
q = 0
while q != None:
  try:
    name1, name2 = map(str, input().split())
    query.append((name1, name2 ))
  except:
    q = None

class GenealogicalTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

nodes = {}
for (descendant, parent) in descendant_parent_pairs:
    # из каждого имени создаем дерево
    if parent not in nodes:
        nodes[parent] = GenealogicalTreeNode(parent)
    if descendant not in nodes:
        nodes[descendant] = GenealogicalTreeNode(descendant)

    # добавляем для каждого имени его потомка
    nodes[parent].children.append(nodes[descendant])

res1 = set()  # Set to keep track of visited nodes of graph.

def dfs1(visited, nodes, node, val):  #function for dfs
    for neighbour in nodes[node].children:
        if neighbour.name != val:
            dfs1(visited, nodes, neighbour.name, val)
        else:
            res1.add(1)

res2 = set()
def dfs2(visited, nodes, node, val):  #function for dfs
    for neighbour in nodes[node].children:
        if neighbour.name != val:
            dfs2(visited, nodes, neighbour.name, val)
        else:
            visited.add(1)

# query = [("Anna", "Nicholaus_I"),("Peter_II", "Peter_I"), ("Alexei", "Paul_I")]

for (name1, name2) in query:
    res1 = set()
    res2 = set()
    dfs1(res1, nodes, name1, name2)
    dfs2(res2, nodes, name2, name1)
    #print(res1, res2)

    if len(res1) == 0 and len(res2) == 0:
        print(0)
    elif len(res1) == 1 and len(res2) == 0:
        print(1)
    elif len(res1) == 0 and len(res2) == 1:
        print(2)


'''
graph = nodes['Peter_I']
visited = set() # Set to keep track of visited nodes of graph.


def dfs(visited, graph, node, val):  #function for dfs
    for neighbour in graph.children:
        if neighbour.name != val:
            dfs(visited, neighbour, neighbour.name, val)
        else:
            visited.add(1)


# Driver Code
print("Following is the Depth-First Search")
print(dfs(visited, graph, 'Paul_I', "Peter_III"))
print(visited)

'''