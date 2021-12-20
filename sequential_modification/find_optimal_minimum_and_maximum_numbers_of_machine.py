from sequential_modification.algorithmOfParalleltask import *
import numpy as np
import itertools


data_list = data

def find_common_price(data_table, pricesOfUsingMachines):
    overall_price = 0
    if type(data_table["idOfMachine"]) == list:
        for m in data_table["idOfMachine"]:
            overall_price += pricesOfUsingMachines[m] * data_table["executingTime"]
        return overall_price
    return pricesOfUsingMachines[data_table["idOfMachine"]] * data_table["executingTime"]


def define_priority_of_tasks(task_graph, data_table):
    longest_path_length = lambda target: len(
        max(nx.all_simple_paths(task_graph, source=0, target=target), key=lambda x: len(x), default=[0])) - 1
    data_table["priority"] = data_table["indexOfTask"].map(longest_path_length)
    return data_table

'''
number_of_machine = 1
pricesOfUsingMachines = {}
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    # id of machine, id of configuration, number of cpu
    machine = ConfigurationOfMachines(i, 1, 4)
    machines.add_machine(machine)
    pricesOfUsingMachines[machine.id] = machine.price
machines.add_switch(switch)
common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
price_of_all_working = sum(scheduling_table.apply(find_common_price, axis=1)) + sum(scheduling_table["transferPrice"])
print('common_time', common_time, 'price_of_all_working', price_of_all_working)
'''

CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              key=lambda tup: tup[0])

data_list = data
# define task

def define_task():
    data = data_list

    descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask",
                                                     "complexityPerUnitOfmemory", "incomingMemory",
                                                     "outgoingMemory", "possibilityOfParalleling",
                                                     "idOfMachine", "start_time_working_of_machine",
                                                     "startTime", "endTime", "executingTimeWithoutTransfer",
                                                     "executingTimeWithTransfer", "executingPrice",
                                                     "transferTime", "transferPrice", "done"])


    number_of_task = len(data)
    taskGraph = set_task(number_of_task)

    descriptionOffTask = define_priority_of_tasks(taskGraph, descriptionOffTask)


    return taskGraph, descriptionOffTask


def from_list_machine_configuration(list_of_seq_machine, list_of_parallel_machine, id_of_switch_seq=1):

    pricesOfUsingMachines = {}
    # print(number_of_machine)
    machines_for_sequential = SetOfMachines(len(list_of_seq_machine))
    switch = ConfigurationOfSwitches(id_of_switch_seq)
    id_of_seq_machine = 1

    for i in list_of_seq_machine:
        machine = ConfigurationOfMachines(id_of_seq_machine, i[1], i[0])
        machines_for_sequential.add_machine(machine)
        machine_price = machine.price
        pricesOfUsingMachines[machine.id] = machine.price
        id_of_seq_machine += 1

    id_of_conf = len(list_of_seq_machine)
    machines_for_sequential.add_switch(switch)
    # configuration for parallel machine
    machines_for_parallel = SetOfMachines(len(list_of_parallel_machine) + 1)
    switch = ConfigurationOfSwitches(len(list_of_parallel_machine) + 1)

    for i, already_added in enumerate(list_of_parallel_machine):
        # taskGraph, descriptionOffTask = define_task()
        machine = ConfigurationOfMachines(i + len(list_of_seq_machine) + 1, already_added[1], already_added[0])
        machines_for_parallel.add_machine(machine)

        pricesOfUsingMachines[machine.id] = machine.price
        id_of_conf = i + len(list_of_seq_machine) + 1

    machines_for_parallel.add_switch(switch)

    return machines_for_parallel, machines_for_sequential


list_min_seq = [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)]
list_min_parallel = [(2, 1)]


def interval_price(list_min_seq, list_min_parallel):
    taskGraph, descriptionOffTask = define_task()
    machines_for_parallel, machines_for_sequential = from_list_machine_configuration(list_min_seq, list_min_parallel)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask,
                                                                   machines_for_sequential, machines_for_parallel)
    # print(common_time)
    sequential_table = scheduling_table[scheduling_table["possibilityOfParalleling"] < 0.3]
    price_of_seq_working = sum(sequential_table["executingPrice"]) + sum(sequential_table["transferPrice"])

    parallelel_table = scheduling_table[scheduling_table["possibilityOfParalleling"] >= 0.3]
    price_of_par_working = sum(parallelel_table["executingPrice"]) + sum(parallelel_table["transferPrice"])
    # print(price_of_par_working, price_of_seq_working)

    return price_of_par_working, price_of_seq_working




def proportion_of_price_for_different_type_of_tasks(price_limit, proportion_of_parallel_tasks, proportion_of_sequential_tasks):
    sum_complexity_parallel = descriptionOffTask[descriptionOffTask["possibilityOfParalleling"] > 0.3]["complexityOfTask"].sum()
    sum_complexity_sequent = descriptionOffTask[descriptionOffTask["possibilityOfParalleling"] <= 0.3]["complexityOfTask"].sum()


    # рассчитываем стоимость для минимального набора машин
    price_of_par_working, price_of_seq_working = interval_price(list_min_seq, list_min_parallel)

    # если сумма стоимостей больше предела цены, то возвращаем нули
    if (price_of_par_working + price_of_seq_working) > price_limit:
        return 0, 0

    coef_seq = price_of_seq_working / price_of_par_working
    print(coef_seq)


    if coef_seq < 0.3:
        coef_seq = coef_seq * 16
    elif coef_seq > 0.3 and coef_seq < 0.6:
        coef_seq = coef_seq * 16
    elif coef_seq > 0.6 and coef_seq < 0.9:
        coef_seq = coef_seq * 8
    elif coef_seq > 0.9 and coef_seq < 1.1:
        coef_seq = coef_seq * 2
    elif coef_seq > 1.1 and coef_seq < 1.5:
        coef_seq = coef_seq * 8
    elif coef_seq > 1.5 and coef_seq < 2:
        coef_seq = coef_seq * 16
    elif coef_seq > 2:
        coef_seq = coef_seq * 32
    else:
        coef_seq = coef_seq
    '''
    if coef_seq  < 1.1 and coef_seq > 0.9:
        coef_seq = coef_seq * 2

    elif coef_seq < 0.9 and coef_seq > 0.3:
        coef_seq = coef_seq * 8
    elif coef_seq < 0.3:
        coef_seq = coef_seq
    elif coef_seq > 1.2:
        coef_seq = 16 * coef_seq
    else:
        coef_seq = coef_seq
    '''

    print(coef_seq)

    common_price_for_all_sequential_tasks = price_limit * proportion_of_sequential_tasks * coef_seq

    if common_price_for_all_sequential_tasks < price_of_seq_working:
        common_price_for_all_sequential_tasks = price_of_seq_working

    common_price_for_all_parallel_tasks = price_limit - common_price_for_all_sequential_tasks

    if common_price_for_all_parallel_tasks < price_of_par_working:
        common_price_for_all_parallel_tasks = price_of_par_working
        common_price_for_all_sequential_tasks = price_limit - common_price_for_all_parallel_tasks

    return common_price_for_all_sequential_tasks, common_price_for_all_parallel_tasks


'''
define maximum number of machine, that can be using
this can be calculated as calculating the cost of computing a task on machines with the cheapest configuration
'''


def max_number_of_machine(price_limit, sorted_list_of_configuration_machine, index_of_configuration):
    try:
        working_price = math.inf
        number_of_machine = 16
        available_number_of_machine = 16

        while working_price > price_limit:
            # set graph of task (sequential)
            pricesOfUsingMachines = {}
            machines = SetOfMachines(number_of_machine)
            switch = ConfigurationOfSwitches(number_of_machine)
            for i in range(1, number_of_machine + 1):
                taskGraph, descriptionOffTask = define_task()

                # id of machine, id of configuration, number of cpu
                machine = ConfigurationOfMachines(i, sorted_list_of_configuration_machine[index_of_configuration][1],
                                                  sorted_list_of_configuration_machine[index_of_configuration][0])
                machines.add_machine(machine)
                pricesOfUsingMachines[machine.id] = machine.price
            machines.add_switch(switch)
            common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, [(2, 1)] ,machines)
            print(number_of_machine)
            price_of_all_working = sum(scheduling_table.apply(
                find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
                scheduling_table["transferPrice"])
            # print('common_time', common_time, 'price_of_all_working', price_of_all_working)
            working_price = price_of_all_working
            # print(number_of_machine, working_price)
            print("w", working_price)
            if working_price <= price_limit:
                available_number_of_machine = number_of_machine
            number_of_machine -= 1

        return available_number_of_machine
    except:
        print("!Increase your budget or simplify the task!")


'''
maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration = max_number_of_machine(10000,
                                                                                   sorted_list_of_configuration_machine,0)
maximum_available_number_of_machines_with_this_price_limit_expensive_configuration = max_number_of_machine(10000,
                                                                                   sorted_list_of_configuration_machine,15)


print("maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration",
      maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration,
      "maximum_available_number_of_machines_with_this_price_limit_expensive_configuration",
      maximum_available_number_of_machines_with_this_price_limit_expensive_configuration, sep="\n")

'''


def transform_table_with_true_start_end_time(scheduling_table_of_current_package):
    scheduling_table_of_current_package = scheduling_table_of_current_package.sort_values(by="indexOfTask")
    # найдем все приоритеты текущей задачи. Следующий приоритет не мождет начаться пока не закончится предыдущий
    priority = list(scheduling_table_of_current_package["priority"].unique())
    print(priority)
    for prior in priority:
        if prior != 0:
            max_prev_prior_time = scheduling_table_of_current_package[scheduling_table_of_current_package["priority"] == prior - 1]["endTime"].max()
            scheduling_table_of_current_package["startTime"] = np.where(
                scheduling_table_of_current_package["priority"] == prior, max_prev_prior_time, scheduling_table_of_current_package["startTime"])

            scheduling_table_of_current_package["endTime"] = scheduling_table_of_current_package["startTime"] + \
                                                             scheduling_table_of_current_package[
                                                                 "executingTime"]


        else:
            scheduling_table_of_current_package["startTime"] = np.where(
                scheduling_table_of_current_package["priority"] == prior, 0, scheduling_table_of_current_package["startTime"])

            scheduling_table_of_current_package["endTime"] = np.where(
                scheduling_table_of_current_package["priority"] == prior, scheduling_table_of_current_package["startTime"] + scheduling_table_of_current_package["executingTime"], 0)


    '''
    priority = list(scheduling_table_of_current_package["priority"].unique())


    for prior in priority:
        if prior != 0:
            max_prev_prior_time = scheduling_table_of_current_package[scheduling_table_of_current_package["priority"] == prior-1]["endTime"].max()


    for prior in priority:
        if prior != 0:
            max_prev_prior_time = scheduling_table_of_current_package[scheduling_table_of_current_package["priority"] == prior-1]["endTime"].max()
            scheduling_table_of_current_package["startTime"] = np.where(
                scheduling_table_of_current_package["priority"] == prior, max_prev_prior_time, scheduling_table_of_current_package["startTime"])

            print(max_prev_prior_time)
        else:
            scheduling_table_of_current_package["startTime"] = np.where(
                scheduling_table_of_current_package["priority"] == prior, 0, scheduling_table_of_current_package["startTime"])


    scheduling_table_of_current_package["endTime"] = scheduling_table_of_current_package["startTime"] + scheduling_table_of_current_package["executingTimeWithoutTransfer"]

    '''



    # for sequential task
    """
    scheduling_table_of_current_package["endTime"] = scheduling_table_of_current_package["endTime"].cumsum()

    scheduling_table_of_current_package["startTime"] = scheduling_table_of_current_package["endTime"].shift(periods=1,
                                                                                                     fill_value=0)

    """
    return scheduling_table_of_current_package