from parallel_task_scheduling.algorithmOfParalleltask import *
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