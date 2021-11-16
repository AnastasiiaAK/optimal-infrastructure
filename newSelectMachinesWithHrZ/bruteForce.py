# слишком долго
'''

from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *




CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 40000

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)), reverse=True)

def calculate_time_and_price_of_current_set_of_machines(sample_of_machines):
    lenght_of_variation = sum(sample_of_machines)

    pricesOfUsingMachines = {}
    machines = SetOfMachines(lenght_of_variation)
    switch = ConfigurationOfSwitches(lenght_of_variation)
    # print(number_of_machine)
    id_of_conf = 0
    taskGraph, descriptionOffTask = define_task()
    id_of_machine = 1

    for i, numbers_of_machines in enumerate(sample_of_machines):
        taskGraph, descriptionOffTask = define_task()
        for _ in range(numbers_of_machines):
            # print(id_of_machine)
            machine = ConfigurationOfMachines(id_of_machine, sorted_list_of_configuration_machine[i][1], sorted_list_of_configuration_machine[i][0])
            machines.add_machine(machine)
            pricesOfUsingMachines[machine.id] = machine.price
            id_of_machine += 1
    machines.add_switch(switch)
    # print(selected_machines)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
    price_of_all_working = sum(scheduling_table.apply(
        find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
        scheduling_table["transferPrice"])

    return common_time, price_of_all_working

for i in range(16):
    for j in range(sorted_list_of_configuration_machine):
        z = j
        while z  < len(sorted_list_of_configuration_machine):
            common_time, price_of_all_working = calculate_time_and_price_of_current_set_of_machines(sample_of_machines)


'''