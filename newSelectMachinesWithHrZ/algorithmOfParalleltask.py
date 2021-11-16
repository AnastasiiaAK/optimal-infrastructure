from algorithmOfSequentialDistribution import *
# from setParallelExecutionOfTask import *
from setTaskSequential import *


# расписание для одной задлачи параллельной или нет
def scheduling_for_sequential_task(task_id, current_time, machines_for_sequential, machines_for_parallel, tasks_dataframe):
    if float(descriptionOffTask.loc[descriptionOffTask["indexOfTask"] == task_id]["possibilityOfParalleling"]) > 0.3:
        current_time = scheduling_for_paralleling_task(task_id, current_time, machines_for_parallel, tasks_dataframe)
    else:
        current_time = scheduling_for_non_paralleling_task(task_id, current_time, machines_for_sequential, tasks_dataframe)
    return current_time


# расписание для задачи, которая делится на несколько подзадач

def scheduling_for_dividing_tasks(id_of_task, current_time, machines_for_sequential, machines_for_parallel, tasks_dataframe, graph):
    # определяем какие задачи должн быть решены

    child_tasks = list(graph.neighbors(id_of_task))
    number_of_child_tasks = len(child_tasks)

    # free_machines = machines.list_of_free_machines(current_time)
    # number_of_free_machines = len(free_machines)
    current_working_time = current_time
    worst_time = 0
    # можем запускать последователдьно, так как задача начинает выпоняться от времени освобождения машины
    for task in child_tasks:
        working_time = scheduling_for_sequential_task(task, current_time, machines_for_sequential, machines_for_parallel, tasks_dataframe)
        current_working_time += working_time
        if current_working_time > worst_time:
            worst_time = current_working_time
    return worst_time



def distribution_tasks_to_machines(graph, dataframe_tasks, machines_for_sequential, machines_for_parallel):
    unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    current_time = 0
    while unperformed_tasks > 0:
        task_id = dataframe_tasks[dataframe_tasks["done"] == "No"]["indexOfTask"].iloc[0]
        parentTask = list(graph.predecessors(task_id))
        if len(parentTask) == 0 or len(list(filter(lambda parent: (dataframe_tasks[dataframe_tasks["indexOfTask"] == parent]["done"] == "No").iloc[0], list(graph.predecessors(task_id))))) == 0:
            if len(list(graph.neighbors(task_id))) == 1 or len(list(graph.neighbors(task_id))) == 0:
                # print("Task:", task_id, "is sequential")
                current_time = scheduling_for_sequential_task(task_id, current_time, machines_for_sequential, machines_for_parallel, dataframe_tasks)
            else:
                # print("Task:", task_id, "is dividing into in several tasks")
                if (dataframe_tasks[dataframe_tasks["indexOfTask"] == task_id]["done"] == "No")[0]:
                    current_time = scheduling_for_sequential_task(task_id, current_time, machines_for_sequential, machines_for_parallel, dataframe_tasks)
                current_time = scheduling_for_dividing_tasks(task_id, current_time, machines_for_sequential, machines_for_parallel, dataframe_tasks, graph)
        unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    common_time_of_working = current_time
    # print("common time of working", common_time_of_working)
    return common_time_of_working, dataframe_tasks


# distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)


#### тестовый вариант !!!!!!!!!!!!!!!!!!!1!!!!!!!!!

# как вариант можно решать не дочерниии задачи конкретной машины, а задачи с определяеным приоритететом


'''

def scheduling_for_dividing_tasks(priority, current_time, machines_for_sequential, machines_for_parallel,
                                  tasks_dataframe, graph):
    # определяем какие задачи должн быть решены
    child_tasks = list(descriptionOffTask[["indexOfTask", "complexityOfTask"]][descriptionOffTask["priority"] == priority].sort_values(by="complexityOfTask", ascending=False)["indexOfTask"])
    number_of_child_tasks = len(child_tasks)
    # можно отсортирвоать по сложности

    # free_machines = machines.list_of_free_machines(current_time)
    # number_of_free_machines = len(free_machines)
    current_working_time = current_time
    worst_time = 0
    # можем запускать последователдьно, так как задача начинает выпоняться от времени освобождения машины
    for task in child_tasks:
        working_time = scheduling_for_sequential_task(task, current_time, machines_for_sequential,
                                                      machines_for_parallel, tasks_dataframe)
        current_working_time += working_time
        if current_working_time > worst_time:
            worst_time = current_working_time
    return worst_time

# execute first task


number_of_machine = 3
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)
current_working_graph = taskGraph


# dont completed tasks
# take first dont completed tasks
#  переаем граф и машины и задачи

# тестовый вариант рапсисания где передаются не задачи, а приоритет

def distribution_tasks_to_machines(graph, dataframe_tasks, machines_for_sequential, machines_for_parallel):
    unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    current_time = 0
    while unperformed_tasks > 0:
        prioritet = dataframe_tasks[dataframe_tasks["done"] == "No"]["priority"].iloc[0]
        print(prioritet)
        current_time = scheduling_for_dividing_tasks(prioritet, current_time, machines_for_sequential, machines_for_parallel,
                                      dataframe_tasks, graph)

        print(current_time)
        unperformed_tasks = len(dataframe_tasks[dataframe_tasks["done"] == "No"])
    common_time_of_working = current_time
    # print("common time of working", common_time_of_working)
    return common_time_of_working, dataframe_tasks


number_of_machine = 4
machines_for_parallel = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines_for_parallel.add_machine(machine)
machines_for_parallel.add_switch(switch)

number_of_machine = 2
machines_for_sequential = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i+4, 1, 4, 'free')
    machines_for_sequential.add_machine(machine)
machines_for_sequential.add_switch(switch)

common_time_of_working, dataframe_tasks = distribution_tasks_to_machines(taskGraphParallel, descriptionOffTask, machines_for_sequential, machines_for_parallel)
print(common_time_of_working, dataframe_tasks)

'''
