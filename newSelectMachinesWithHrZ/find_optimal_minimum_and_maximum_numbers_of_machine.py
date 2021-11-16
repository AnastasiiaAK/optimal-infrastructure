from newSelectMachinesWithHrZ.algorithmOfParalleltask import *
import numpy as np
import itertools


def find_common_price(data_table, pricesOfUsingMachines):
    overall_price = 0
    if type(data_table["idOfMachine"]) == list:
        for m in data_table["idOfMachine"]:
            overall_price += pricesOfUsingMachines[m] * data_table["executingTime"]
        return overall_price
    return pricesOfUsingMachines[data_table["idOfMachine"]] * data_table["executingTime"]


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



# define task
def define_task():
    data = [[0, 0, round(0.11952686309814453, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [1, 1, round(0.38246989250183105, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [2, 2, round(0.0005393028259277344, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [3, 3, round(1.6666145324707031, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [4, 4, round(1451.2022745609283, 2), 0, 0, 1, None, None, None, None, None, "No"],
            [5, 5, round(0.67854, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [6, 6, round(0.4834657, 2), 0, 0, 0, None, None, None, None, None, "No"]]
    number_of_task = len(data)
    taskGraph = set_task(number_of_task)

    descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask", "incomingMemory",
                                                     "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                                     "startTime", "endTime", "executingTime", "transferPrice", "done"])

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