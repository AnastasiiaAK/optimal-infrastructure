from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *
from newSelectMachinesWithHrZ.greedyAlgorithm import greedy_algorithm_for_sequential_tasks

price_limit = 10000
CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
max_number_of_sequential_machine = 1

selected_machines_sequential = greedy_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit)


def config_sequential_machine(selected_machines_sequential):
    pricesOfUsingMachines = {}
    machines_for_sequential = SetOfMachines(len(selected_machines_sequential))
    switch = ConfigurationOfSwitches(len(selected_machines_sequential))
    machine = ConfigurationOfMachines(len(selected_machines_sequential), selected_machines_sequential[0][1],
                                      selected_machines_sequential[0][0])
    machines_for_sequential.add_machine(machine)
    machine_price = machine.price
    machines_for_sequential.add_switch(switch)
    pricesOfUsingMachines[machine.id] = machine.price

    return machines_for_sequential, pricesOfUsingMachines



sorted_list_of_configuration_machine_parallel = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine_parallel = sorted(
    list(itertools.chain(*sorted_list_of_configuration_machine_parallel)), reverse=True)

# набор самых быстрых машин стоимости до i. (с наименьшим временем выпаолнеенияя)

# при i = 0 => time = inf, набор машин = 0
'''
первое i - это стоимость самой дешевой машины за 1 минуту
шаг стоимости можно обозначить как 100
'''

list_price_limits = list(range(0, price_limit + 100, 100))
sorted_list_of_configuration_machine_parallel # они отсортированы по стоимости и конфигурации одновременно
list_price_machines_for_each_price = [math.inf] * len(list_price_limits)
list_set_for_each_price = [[] for _ in range(len(list_price_limits))]

machines_for_sequential, pricesOfUsingMachines = config_sequential_machine(selected_machines_sequential)
for price in list_price_limits:
    for potent_machine in sorted_list_of_configuration_machine_parallel:
        machines_for_sequential, pricesOfUsingMachines = config_sequential_machine(selected_machines_sequential)

        taskGraph, descriptionOffTask = define_task()
        current_set_of_machines = SetOfMachines(1)
        current_switch = ConfigurationOfSwitches(1)
        current_machine = ConfigurationOfMachines(2, potent_machine[1], potent_machine[0])
        current_set_of_machines.add_machine(current_machine)
        current_set_of_machines.add_switch(current_switch)
        pricesOfUsingMachines[current_machine.id] = current_machine.price
        common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask,
                                                                       machines_for_sequential, current_set_of_machines)
        price_of_using_this_machine = sum(scheduling_table.apply(
            find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
            scheduling_table["transferPrice"])

        index_price = price // 100

        if price_of_using_this_machine <= price:

            # делаем вычисление толсько на текущей машине на одной
            list_price_machines_for_each_price[index_price] = min(list_price_machines_for_each_price[index_price],
            #                                                      common_time)

            list_set_for_each_price[index_price].append(potent_machine)



            print(list_set_for_each_price[index_price])


            # здесь пытаемся ее прибавить к преддущей конфигурации

            taskGraph, descriptionOffTask = define_task()
            index_price = price // 100
            # найти индекс ближайшего списка без текущей машины
            '''
            try:
            
                # мф должны найти наименьший сет, где без стоимоти текущей машины, а не без текущей машины
                # текущая стоимoсть - стоимость текущей машины
                for ind, conf in enumerate(list_set_for_each_price[::-1]):
                    if potent_machine in conf:
                        count_index_price_without_current_machine = conf.count(potent_machine)
                        print("po")
                        break
                    else:
                        index_price_without_current_machine = index_price - 1

                for ind, conf in enumerate(list_set_for_each_price[::-1]):
                    if conf.count(potent_machine) == count_index_price_without_current_machine - 1:
                        index_price_without_current_machine = ind
                        print("ok")
                        break

                if index_price_without_current_machine is None:
                    index_price_without_current_machine = 0

            except:
                # index_price_without_current_machine = 0
                index_price_without_current_machine = 0
            '''

            index_price_without_current_machine = price - int(price_of_using_this_machine // 1000) * 10
            print(price, int(price_of_using_this_machine // 1000) * 100)
            # прсто возьмем предыдущую конфигураицю и будем подставлять следующую машину, если они проходят по цене, то ок,  если нет то оставляем текущую машину
            a = list_set_for_each_price[index_price_without_current_machine]
            current_list_set_of_machine = a[:]
            current_list_set_of_machine.append(potent_machine)
            print(current_list_set_of_machine)
            machines_for_sequential, pricesOfUsingMachines = config_sequential_machine(selected_machines_sequential)
            current_set_of_machines = SetOfMachines(len(current_list_set_of_machine))
            current_switch = ConfigurationOfSwitches(len(current_list_set_of_machine))
            # print(current_list_set_of_machine)
            for ind, conf in enumerate(current_list_set_of_machine):
                current_machine = ConfigurationOfMachines(ind + 2, conf[1], conf[0])
                current_set_of_machines.add_machine(current_machine)
                pricesOfUsingMachines[current_machine.id] = current_machine.price
            current_set_of_machines.add_switch(current_switch)

            common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask,
                                                                           machines_for_sequential,
                                                                           current_set_of_machines)

            price_of_using_this_machine = sum(scheduling_table.apply(
                find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
                scheduling_table["transferPrice"])

            if price_of_using_this_machine <= price and len(current_list_set_of_machine) <= 16:
                if common_time < list_price_machines_for_each_price[index_price]:
                    list_set_for_each_price[index_price] = current_list_set_of_machine
                    print("1", current_list_set_of_machine)
                    list_price_machines_for_each_price[index_price] = min(list_price_machines_for_each_price[index_price], common_time)



print(list_set_for_each_price)
print(list_price_machines_for_each_price)
