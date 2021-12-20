from classesOfMacines import *
# from setTaskSequential import *
# from setParallelExecutionOfTask import *
from parameters import dictWithPrices

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

# select machines for task

# наилучшее время выполнения будет при наибольшем кол-ве машин с лучшей конфигурацией
# наихудшее время выполнения будет с одной машиной при самой дешевой конфигурации

# рассматриваем распарралеливание только по CPU в рамках одной машины

# example
# id_of_machine, cpu, core_freq, price, is_available

# data for region Europe(London), OS (Linux)
# 1. M5a (large, xlarge, 2xlarge, 4xlarge)

# 2. M5 (large, xlarge, 2xlarge, 4xlarge)
# 3. C5n (large, xlarge, 2xlarge, 4xlarge)
# 4. r5b (large, xlarge, 2xlarge, 4xlarge)

'''
CPU = [2, 4, 8, 16]

coreFreq1 = 2.5
coreFreq2 = 3.1
coreFreq3 = 3.4
coreFreq4 = 3.5
dictWithPrices = {'1': {'2': 0.11, '4': 0.24, '8': 0.56, '16': 1.44},
                  '2': {'2': 0.123, '4': 0.272, '8': 0.642,'16': 1.682},
                  '3': {'2': 0.142, '4': 0.31, '8': 0.73, '16': 1.894},
                  '4': {'2': 0.189, '4': 0.406, '8': 0.924, '16': 2.296}}

dictFreq = {'1': 2.5, '2': 3.1, '3': 3.4, "4": 3.5}

'''

'''
number_of_machine = 3
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)
'''

# for firstTask
# set currentTime - time of executing of all tasks
# set timeOfExecutingTask - working time for 1 task = time of work + time for transfer


def scheduling_for_non_paralleling_task(id_of_task, current_time, machines, tasks_dataframe):

    # найти количество машин одновременно передающих (машин с одним уровнем приоритета)
    priority_of_current_task = tasks_dataframe[tasks_dataframe["indexOfTask"] == id_of_task]["priority"].values[0]
    number_of_machine_in_priority = len(tasks_dataframe[(tasks_dataframe["priority"] == priority_of_current_task) & (tasks_dataframe["possibilityOfParalleling"] < 0.3)])

    number_of_machine = min(machines.switch.attached_devices, number_of_machine_in_priority)


    '''
    сделаем для задач, количество которых больше количества  возможных машин у свитча прибавление во времени передачи (только туда)
    '''
    # определим количество задач и названия, которые имеют одинаковый приоритет. Они приходят в порядке возрастания сложности
    priority_of_current_task = tasks_dataframe[tasks_dataframe["indexOfTask"] == id_of_task]["priority"].values[0]
    number_of_machine_in_priority = len(tasks_dataframe[(tasks_dataframe["priority"] == priority_of_current_task) & (tasks_dataframe["possibilityOfParalleling"] < 0.3)])
    names = tasks_dataframe[(tasks_dataframe["priority"] == priority_of_current_task) & (tasks_dataframe["possibilityOfParalleling"] < 0.3)]["nameOfTask"].values
    # сделаем словарь с прибавкой ко времени передачи
    # (то есть для таких задач время трансфера будет равно времени трансфера плюс время ожидания)
    dictAwaiting = {}
    for order, name in enumerate(names):
        queue = order // machines.switch.attached_devices
        if queue > 0:
            begin_id = (queue-1) * machines.switch.attached_devices
            end_id = min(begin_id + machines.switch.attached_devices, len(names))
            id_of_task_with_max_memory = tasks_dataframe[tasks_dataframe["nameOfTask"].isin(names[begin_id:end_id])]["incomingMemory"].idxmax()
            dictAwaiting[name] = {}
            dictAwaiting[name]["awaitingTime"] = machines.switch.calculate_transfer_time(number_of_machine, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task_with_max_memory])
            dictAwaiting[name]["number_task_same_time"] = min(begin_id + machines.switch.attached_devices, len(names)) - begin_id
        else:
            dictAwaiting[name] = {}
            dictAwaiting[name]["awaitingTime"] = 0
            dictAwaiting[name]["number_task_same_time"] = min(machines.switch.attached_devices, number_of_machine_in_priority)


    number_of_machine = dictAwaiting[tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]["nameOfTask"].values[0]]["number_task_same_time"]

    awaiting_time = dictAwaiting[tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]["nameOfTask"].values[0]]["awaitingTime"]
    # прибавим время ожидания свитча к времени передачи в одну строну

    transfer_time = machines.switch.calculate_transfer_time(number_of_machine, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]) + awaiting_time

    transfer_price = machines.switch.calculate_transfer_price(number_of_machine, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])

    transfer_time1 = machines.switch.calculate_transfer_time_to(number_of_machine, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]) + awaiting_time

    transfer_time2 = machines.switch.calculate_transfer_time_from(number_of_machine, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])

    # find list of free machines
    free_machines = machines.list_of_free_machines(current_time)

    # найдем количество машин одновременно используемых в момент времени
    number_all_machines = len(machines.listOfMachines)

    if len(free_machines) == 0:
        time_of_nearest_free_machine = math.inf
        for device in machines.listOfMachines:
            if time_of_nearest_free_machine > device.time_of_deliverance:
                time_of_nearest_free_machine = device.time_of_deliverance + 0.000001
        current_time = time_of_nearest_free_machine
    free_machines = machines.list_of_free_machines(current_time)
    # choose best machines for solving this task. Choosing best because tasks are performed sequentially

    best_free_machine = machines.find_best_free_machines(tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task], current_time)
    tasks_dataframe.at[id_of_task, "start_time_working_of_machine"] = current_time

    # найдем количество машин одновременно используемых в момент времени
    number_all_machines = len(machines.listOfMachines)
    # if start_time_working_of_machine in previous task is equal to current_time =>


    current_time += transfer_time1


    # define what time this task is executing in this machines  and set this machine for time a busy
    working_time = best_free_machine.working_time_with_particular_task(tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task], float(tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]["complexityOfTask"]))
    # set in dataframe with description of task executing, start, finish time
    tasks_dataframe.at[id_of_task, "executingTimeWithoutTransfer"] = working_time
    tasks_dataframe.at[id_of_task, "executingTime"] = working_time + transfer_time1
    tasks_dataframe.at[id_of_task, "executingTimeWithTransfer"] = working_time + transfer_time1 + transfer_time2

    tasks_dataframe.at[id_of_task, "startTime"] = current_time - transfer_time1  # start time (with transfer time to begin)
    current_time += working_time

    best_free_machine.make_machine_busy(current_time + transfer_time2)

    tasks_dataframe.at[id_of_task, "endTime"] = current_time + transfer_time2

    # tasks_dataframe.at[id_of_task, "endTime"] = working_time + transfer_time1

    tasks_dataframe.at[id_of_task, "idOfMachine"] = best_free_machine.id
    tasks_dataframe.at[id_of_task, "done"] = "Yes"
    tasks_dataframe.at[id_of_task, "transferPrice"] = transfer_price
    tasks_dataframe.at[id_of_task, "executingPrice"] = (working_time + transfer_time1 + transfer_time2) * dictWithPrices[best_free_machine.id_of_configuration][best_free_machine.CPU] * 60  # умножаем на 60 для перевода в другую метрику
    # tasks_dataframe.at[id_of_task, "transferTime"] = transfer_time1 + transfer_time2
    tasks_dataframe.at[id_of_task, "transferTime"] = transfer_time1 + transfer_time2

    best_free_machine.make_machine_free()

    return current_time


def scheduling_for_paralleling_task(id_of_task, current_time, machines, tasks_dataframe):
    # find list of free machines
    free_machines = machines.list_of_free_machines(current_time)

    # it can be replace to function of set current_time as the time of first vacated machine
    '''
    if len(free_machines) == 0:
        while machines.list_of_free_machines(current_time) == 0:
            current_time += 1
    '''

    if len(free_machines) == 0:
        time_of_nearest_free_machine = math.inf
        for device in machines.listOfMachines:
            if time_of_nearest_free_machine > device.time_of_deliverance:
                time_of_nearest_free_machine = device.time_of_deliverance + 0.000001
        current_time = time_of_nearest_free_machine
    free_machines = machines.list_of_free_machines(current_time)
    number_of_free_machines = len(free_machines)
    tasks_dataframe.at[id_of_task, "start_time_working_of_machine"] = current_time

    transfer_time = machines.switch.calculate_transfer_time(
        number_of_free_machines, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])

    transfer_time1 = machines.switch.calculate_transfer_time_to(number_of_free_machines, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])
    transfer_time2 = machines.switch.calculate_transfer_time_from(number_of_free_machines, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])

    current_time += transfer_time
    transfer_price = machines.switch.calculate_transfer_price(
        number_of_free_machines, tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task])

    # we can distribute task to machines according its cpu (in order for the machines to preform tasks about same time)
    common_cpu = 0
    list_id_of_free_machines = []
    for i in free_machines:
        common_cpu += i.CPU * i.core_freq
        list_id_of_free_machines.append(i.id)
    worst_time = 0
    current_executing_price = 0

    for parallel_machine in free_machines:
        current_time_for_parallel = current_time
        working_time = parallel_machine.working_time_with_particular_task(
            tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task],
            (parallel_machine.CPU * parallel_machine.core_freq) / common_cpu * float(tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == id_of_task]["complexityOfTask"]))

        part_of_task = parallel_machine.CPU * parallel_machine.core_freq / common_cpu

        current_executing_price += (working_time + transfer_time1 * part_of_task + transfer_time2 * part_of_task) * dictWithPrices[parallel_machine.id_of_configuration][parallel_machine.CPU]

        if working_time > worst_time:
            worst_time = working_time
        parallel_machine.make_machine_busy(working_time + current_time_for_parallel)
        parallel_machine.make_machine_free()


    tasks_dataframe.at[id_of_task, "executingTimeWithoutTransfer"] = worst_time # time without transfer

    tasks_dataframe.at[id_of_task, "executingTime"] = worst_time + transfer_time1  # time with transfer to machine
    tasks_dataframe.at[id_of_task, "startTime"] = current_time - transfer_time1  # start time with time for transfer
    current_time += worst_time

    tasks_dataframe.at[id_of_task, "endTime"] = current_time + transfer_time2

    tasks_dataframe.at[id_of_task, "idOfMachine"] = list_id_of_free_machines
    tasks_dataframe.at[id_of_task, "done"] = "Yes"
    tasks_dataframe.at[id_of_task, "transferPrice"] = transfer_price
    tasks_dataframe.at[id_of_task, "transferTime"] = transfer_time1 + transfer_time2
    tasks_dataframe.at[id_of_task, "executingTimeWithTransfer"] = worst_time + transfer_time1 + transfer_time2  # time with transfers both

    tasks_dataframe.at[id_of_task, "executingPrice"] = current_executing_price * 60  # умножаем на 60 для перевода в другую метрику
    # tasks_dataframe.at[id_of_task, "transferTime"] = transfer_time1

    return current_time


'''
current_time = 0
for task_id in tasks_dataframe["indexOfTask"]:
    if float(tasks_dataframe.loc[tasks_dataframe["indexOfTask"] == task_id]["possibilityOfParalleling"]) > 0.3:
        current_time = scheduling_for_paralleling_task(task_id, current_time)
    else:
        current_time = scheduling_for_non_paralleling_task(task_id, current_time)

time_to_complete_all_tasks = current_time
print("time_to_complete_all_tasks", time_to_complete_all_tasks, "sec")

'''

