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
    assert (nx.is_directed_acyclic_graph(g))  # check if graph is DAG

    # nx.draw(g, with_labels=True)  # draw
    # plt.title("Sequential task")
    # plt.show()
    return g


def define_priority_of_tasks(task_graph, data_table):
    longest_path_length = lambda target: len(
        max(nx.all_simple_paths(task_graph, source=0, target=target), key=lambda x: len(x), default=[0])) - 1
    descriptionOffTask["priority"] = descriptionOffTask["indexOfTask"].map(longest_path_length)
    return data_table


# set number of task
number_of_task = 7

# set graph of task (sequential)

# set number of task
# set graph of task (sequential)
taskGraphParallel = set_task(number_of_task)

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


data = [
    [0, 0, round(0.11952686309814453, 2), 0.119 / 300, 300, 200, 0, None, None, None, None, None, None, None,  None, None,
     "No"],
    [1, 1, round(0.38246989250183105, 2), 0.3824 / 200, 200, 500, 0, None, None, None, None, None, None, None,  None, None,
     "No"],
    [2, 2, round(0.0005393028259277344, 4), 0.0005393 / 500, 500, 1000, 0, None, None, None, None, None, None,  None, None,
     None, "No"],
    [3, 3, round(1.6666145324707031, 2), 1.66661 / 1000, 1000, 780, 0, None, None, None, None, None, None, None, None,
     None, "No"],
    [4, 4, round(1451.2022745609283, 2), 1451.2022 / 780, 780, 880, 1, None, None, None, None, None, None,  None, None,
     None, "No"],
    [5, 5, round(0.67854, 2), 0.67854 / 880, 880, 200, 0, None, None, None, None, None, None, None, None,  None, "No"],
    [6, 6, round(0.4834657, 2), 0.48346 / 200, 200, 0, 0, None, None, None, None, None, None, None, None, None, "No"]]

descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask",
                                                 "complexityPerUnitOfmemory", "incomingMemory",
                                                 "outgoingMemory", "possibilityOfParalleling",
                                                 "idOfMachine", "start_time_working_of_machine",
                                                 "startTime", "endTime", "executingTimeWithoutTransfer",
                                                 "executingTimeWithTransfer", "executingPrice",
                                                 "transferTime", "transferPrice", "done"])


# calculate the proportion of sequential tasks and parallel tasks
descriptionOffTask = define_priority_of_tasks(taskGraphParallel, descriptionOffTask)


proportion_of_parallel_tasks = round(descriptionOffTask
                                     [descriptionOffTask["possibilityOfParalleling"] > 0.3]["complexityOfTask"].sum()
                                     / descriptionOffTask["complexityOfTask"].sum(), 5)

proportion_of_sequential_tasks = round(descriptionOffTask[descriptionOffTask["possibilityOfParalleling"] < 0.3]["complexityOfTask"].sum()
                                       / descriptionOffTask["complexityOfTask"].sum(), 5)





def proportion_of_price_for_different_type_of_tasks(price_limit, proportion_of_parallel_tasks, proportion_of_sequential_tasks):
    common_price_for_all_sequentuial_tasks = price_limit * proportion_of_sequential_tasks * 16
    common_price_for_all_parallel_tasks = price_limit - common_price_for_all_sequentuial_tasks
    return common_price_for_all_sequentuial_tasks, common_price_for_all_parallel_tasks


print(proportion_of_price_for_different_type_of_tasks(1000, proportion_of_parallel_tasks, proportion_of_sequential_tasks))


def find_max_number_of_machine_for_sequential(descriptionOffTask):
    table_sequential = descriptionOffTask[descriptionOffTask["possibilityOfParalleling"] < 0.3]
    max_number_of_seq_machine = table_sequential["priority"].value_counts(sort=True).iloc[0]
    return max_number_of_seq_machine


max_number_of_sequential_machine = find_max_number_of_machine_for_sequential(descriptionOffTask)

