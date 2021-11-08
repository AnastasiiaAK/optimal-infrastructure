from algorithmOfSequentialDistribution import *
# from setParallelExecutionOfTask import *
from setTaskSequential import *


def scheduling_for_sequential_task(task_id, current_time, machines, tasks_dataframe):
    if float(descriptionOffTask.loc[descriptionOffTask["indexOfTask"] == task_id]["possibilityOfParalleling"]) > 0.3:
        current_time = scheduling_for_paralleling_task(task_id, current_time, machines, tasks_dataframe)
    else:
        current_time = scheduling_for_non_paralleling_task(task_id, current_time, machines, tasks_dataframe)
    return current_time


def scheduling_for_dividing_tasks(id_of_task, current_time, machines, tasks_dataframe, graph):
    child_tasks = list(graph.neighbors(id_of_task))
    number_of_child_tasks = len(child_tasks)

    free_machines = machines.list_of_free_machines(current_time)
    number_of_free_machines = len(free_machines)
    current_working_time = current_time
    worst_time = 0
    for task in child_tasks:
        working_time = scheduling_for_sequential_task(task, current_time, machines, tasks_dataframe)
        current_working_time += working_time
        if current_working_time > worst_time:
            worst_time = current_working_time
    return worst_time


# execute first task

'''
number_of_machine = 3
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)
current_working_graph = taskGraph
'''

# dont completed tasks
# take first dont completed tasks
#  переаем граф и машины и задачи


def distribution_tasks_to_machines(graph, dataframe_tasks, given_machines):
    unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    current_time = 0
    while unperformed_tasks > 0:
        task_id = dataframe_tasks[dataframe_tasks["done"] == "No"]["indexOfTask"].iloc[0]
        parentTask = list(graph.predecessors(task_id))
        if len(parentTask) == 0 or len(list(filter(lambda parent: (dataframe_tasks[dataframe_tasks["indexOfTask"] == parent]["done"] == "No").iloc[0], list(graph.predecessors(task_id))))) == 0:
            if len(list(graph.neighbors(task_id))) == 1 or len(list(graph.neighbors(task_id))) == 0:
                # print("Task:", task_id, "is sequential")
                current_time = scheduling_for_sequential_task(task_id, current_time, given_machines, dataframe_tasks)
            else:
                # print("Task:", task_id, "is dividing into in several tasks")
                if (dataframe_tasks[dataframe_tasks["indexOfTask"] == task_id]["done"] == "No")[0]:
                    current_time = scheduling_for_sequential_task(task_id, current_time, given_machines, dataframe_tasks)
                current_time = scheduling_for_dividing_tasks(task_id, current_time, given_machines, dataframe_tasks, graph)
        unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    common_time_of_working = current_time
    # print("common time of working", common_time_of_working)
    return common_time_of_working, dataframe_tasks


# distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)


'''
    current_time = 0
    while unperformed_tasks > 0:
        task_id = descriptionOffTask[descriptionOffTask["done"] == "No"]["indexOfTask"].iloc[0]
        parentTask = list(taskGraphParallel.predecessors(task_id))
        if len(parentTask) == 0 or len(list(filter(lambda parent: (descriptionOffTask[descriptionOffTask["indexOfTask"] == parent]["done"] == "No").iloc[0], list(taskGraphParallel.predecessors(task_id))))) == 0:
            if len(list(taskGraphParallel.neighbors(task_id))) == 1 or len(list(taskGraphParallel.neighbors(task_id))) == 0:
                print("Task:", task_id, "is sequential")
                current_time = scheduling_for_sequential_task(task_id, current_time, machines)
                print(current_time)
            else:
                print("Task:", task_id, "is dividing into in several tasks")
                if (descriptionOffTask[descriptionOffTask["indexOfTask"] == task_id]["done"] == "No")[0]:
                    current_time = scheduling_for_sequential_task(task_id, current_time, machines)
                current_time = scheduling_for_dividing_tasks(task_id, current_time, machines)
                print(current_time)
        unperformed_tasks = len(descriptionOffTask[descriptionOffTask["done"] == "No"])
        print(descriptionOffTask)
    common_time_of_working = current_time
    print("common time of working", common_time_of_working)
'''