from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *




CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 20000


def greedy_algorithm_for_configuration_of_machine(CPU, coreFreq, price_limit):
    sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
    sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)), reverse=True)

    # remaining_price = price_limit
    selected_machines = []
    working_time = 0
    number_of_machine = 0
    cost_of_current_package = 0
    working_time_of_current_package = 0
    scheduling_table_of_current_package = pd.DataFrame()

    # for potential_machine in sorted_list_of_configuration_machine:
    itr = iter(sorted_list_of_configuration_machine)
    potential_machine = next(itr)

    try:
        while True:
            # set current configuration of machine
            pricesOfUsingMachines = {}
            machines = SetOfMachines(len(selected_machines) + 1)
            switch = ConfigurationOfSwitches(len(selected_machines) + 1)
            # print(number_of_machine)
            id_of_conf = 0
            taskGraph, descriptionOffTask = define_task()
            for i, already_added in enumerate(selected_machines):
                taskGraph, descriptionOffTask = define_task()
                machine = ConfigurationOfMachines(i, already_added[1], already_added[0])
                machines.add_machine(machine)
                pricesOfUsingMachines[machine.id] = machine.price
                id_of_conf = i

            # id of machine, id of configuration, number of cpu
            machine = ConfigurationOfMachines(id_of_conf + 1, potential_machine[1], potential_machine[0])
            # print(potential_machine)
            machines.add_machine(machine)
            pricesOfUsingMachines[machine.id] = machine.price
            machines.add_switch(switch)
            # print(selected_machines)
            common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
            price_of_all_working = sum(scheduling_table.apply(
                find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
                scheduling_table["transferPrice"])
            # print(price_of_all_working)
            if price_of_all_working < price_limit:
                selected_machines.append(potential_machine)
                number_of_machine = len(selected_machines)
                cost_of_current_package = price_of_all_working
                working_time_of_current_package = common_time
                scheduling_table_of_current_package = scheduling_table

            else:
                potential_machine = next(itr)
                # print(potential_machine)
    except StopIteration:
        print("selected_machines", selected_machines)
        print("price_of_all_working", cost_of_current_package)
        print("working_time_of_best_package", working_time_of_current_package)
        if working_time_of_current_package == 0:
            print("!Increase the price-limit or simplify the task!")
    finally:
        del itr

    return selected_machines, cost_of_current_package, working_time_of_current_package, scheduling_table_of_current_package


CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 6000
price_limit = 7000
selected_machines, cost_of_current_package, working_time_of_current_package, scheduling_table_of_current_package = greedy_algorithm_for_configuration_of_machine(CPU, coreFreq, price_limit)


# from evaluating of effectiveness of working of greedy algorithms xl <= x* <=2xl
# where xl - results of working greedy algorithm


'''
import numpy as np

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              reverse=True)


# scale machines as follows
scaled_selected_machines = np.floor(np.array(sorted_list_of_configuration_machine) / (np.array((16, 4)) * 0.3 / len(sorted_list_of_configuration_machine)))
scaled_selected_machines
'''
