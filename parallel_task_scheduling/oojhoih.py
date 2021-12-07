from newSelectMachinesWithHrZ.algorithmOfParalleltask import *
import numpy as np
import itertools


def find_common_price(data_table):
    overall_price = 0
    if type(data_table["idOfMachine"]) == list:
        for m in data_table["idOfMachine"]:
            overall_price += pricesOfUsingMachines[m] * data_table["executingTime"]
        return overall_price
    return pricesOfUsingMachines[data_table["idOfMachine"]] * data_table["executingTime"]


number_of_task = 7
# set graph of task (sequential)
taskGraph = set_task(number_of_task)

data = [[0, 0, round(0.11952686309814453, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [1, 1, round(0.38246989250183105, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [2, 2, round(0.0005393028259277344, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [3, 3, round(1.6666145324707031, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [4, 4, round(1451.2022745609283, 2), 0, 0, 1, None, None, None, None, None, "No"],
        [5, 5, round(0.67854, 2), 0, 0, 0, None, None, None, None, None, "No"],
        [6, 6, round(0.4834657, 2), 0, 0, 0, None, None, None, None, None, "No"]]

descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask", "incomingMemory",
                                                 "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                                 "startTime", "endTime", "executingTime", "transferPrice", "done"])



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

sorted_lost_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x]*len(CPU))), coreFreq))
sorted_lost_of_configuration_machine = sorted(list(itertools.chain(*sorted_lost_of_configuration_machine)),
                                              key=lambda tup: tup[0])

# find best machine with given price limit



price_limit = 300

best_available_machine = len(sorted_lost_of_configuration_machine)-1
working_price = math.inf
number_of_machine = 1

while working_price > price_limit:
    number_of_task = 7
    # set graph of task (sequential)
    taskGraph = set_task(number_of_task)

    data = [[0, 0, round(0.11952686309814453, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [1, 1, round(0.38246989250183105, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [2, 2, round(0.0005393028259277344, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [3, 3, round(1.6666145324707031, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [4, 4, round(1451.2022745609283, 2), 0, 0, 1, None, None, None, None, None, "No"],
            [5, 5, round(0.67854, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [6, 6, round(0.4834657, 2), 0, 0, 0, None, None, None, None, None, "No"]]

    descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask", "incomingMemory",
                                                     "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                                     "startTime", "endTime", "executingTime", "transferPrice", "done"])

    pricesOfUsingMachines = {}
    machines = SetOfMachines(number_of_machine)
    switch = ConfigurationOfSwitches(number_of_machine)
    for i in range(1, number_of_machine + 1):
        # id of machine, id of configuration, number of cpu
        machine = ConfigurationOfMachines(i, sorted_lost_of_configuration_machine[best_available_machine][1], sorted_lost_of_configuration_machine[best_available_machine][0])
        machines.add_machine(machine)
        pricesOfUsingMachines[machine.id] = machine.price
    machines.add_switch(switch)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
    price_of_all_working = sum(scheduling_table.apply(find_common_price, axis=1)) + sum(
        scheduling_table["transferPrice"])
    print('common_time', common_time, 'price_of_all_working', price_of_all_working)
    working_price = price_of_all_working
    best_available_machine -= 1

print(best_available_machine, sorted_lost_of_configuration_machine[best_available_machine])
print("number_of_cpu", sorted_lost_of_configuration_machine[best_available_machine][0], "frequency", coreFreqValues[sorted_lost_of_configuration_machine[best_available_machine][1]])


# def best_car_with_considered_price()