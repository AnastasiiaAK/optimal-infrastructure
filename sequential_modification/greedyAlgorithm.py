from sequential_modification.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, transform_table_with_true_start_end_time, from_list_machine_configuration, proportion_of_price_for_different_type_of_tasks, list_min_seq, list_min_parallel
import itertools
from sequential_modification.algorithmOfParalleltask import *


CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 9000
max_number_of_sequential_machine = len(descriptionOffTask[descriptionOffTask["possibilityOfParalleling"] < 0.3])  # количество задач без возможности распараллеливания




def greedy_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit, max_number_of_sequential_machine):
    sorted_list_of_configuration_machine_sequential = list(map(lambda x: list(zip([min(CPU)], [x])), coreFreq))
    sorted_list_of_configuration_machine_sequential = sorted(
        list(itertools.chain(*sorted_list_of_configuration_machine_sequential)), reverse=True)

    common_price_for_all_sequential_tasks, common_price_for_all_parallel_tasks = proportion_of_price_for_different_type_of_tasks(
        price_limit, proportion_of_parallel_tasks, proportion_of_sequential_tasks)

    # если стоимость расчетов на самых худших машинах меньше предела цены, то выводим сообщение в ошибке

    if common_price_for_all_sequential_tasks == 0 and common_price_for_all_parallel_tasks == 0:
        raise ValueError("Increase the price-limit or simplify the task")



    iter_sequential = iter(sorted_list_of_configuration_machine_sequential)
    potential_machine = next(iter_sequential)
    selected_machines_sequential = []
    number_of_machine = 0
    global working_time_of_current_package
    working_time_of_current_package = math.inf
    taskGraph, descriptionOffTask = define_task()

    try:
        while True and number_of_machine <= max_number_of_sequential_machine:
            machines_for_parallel, machines_for_sequential = from_list_machine_configuration(selected_machines_sequential, [(2,1)])
            taskGraph, descriptionOffTask = define_task()
            id_of_conf = len(selected_machines_sequential) + 1
            # id of machine, id of configuration, number of cpu
            machine = ConfigurationOfMachines(id_of_conf + 1, potential_machine[1], potential_machine[0])
            # print(potential_machine)
            machines_for_sequential.add_machine(machine)
            # pricesOfUsingMachines[machine.id] = machine.price
            # print(selected_machines)
            common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines_for_sequential, machines_for_parallel)
            sequential_table = scheduling_table[scheduling_table["possibilityOfParalleling"] < 0.3]
            price_of_seq_working = sum(sequential_table["executingPrice"]) + sum(sequential_table["transferPrice"])


            if price_of_seq_working < common_price_for_all_sequential_tasks:
                selected_machines_sequential.append(potential_machine)
                number_of_machine = len(selected_machines_sequential) + 1
                cost_of_current_package = price_of_seq_working
                working_time_of_current_package = common_time
                scheduling_table_of_current_package = scheduling_table
                iter_sequential = iter(sorted_list_of_configuration_machine_sequential)
                potential_machine = next(iter_sequential)
            else:
                potential_machine = next(iter_sequential)
                # print(potential_machine)

        if working_time_of_current_package > 0:
            selected_machines_sequential

    except StopIteration:
        if working_time_of_current_package == math.inf:
            selected_machines_sequential = [sorted_list_of_configuration_machine_sequential[-1]] * max_number_of_sequential_machine

    finally:
        del iter_sequential

    return selected_machines_sequential







def analytical_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit):

    # список машин для последовательного вычиления без распараллеливания
    sorted_list_of_configuration_machine_sequential = list(map(lambda x: list(zip([min(CPU)], [x])), coreFreq))
    sorted_list_of_configuration_machine_sequential = sorted(
        list(itertools.chain(*sorted_list_of_configuration_machine_sequential)), reverse=True)

    common_price_for_all_sequentuial_tasks, common_price_for_all_parallel_tasks = proportion_of_price_for_different_type_of_tasks(price_limit, proportion_of_parallel_tasks, proportion_of_sequential_tasks)

    taskGraph, descriptionOffTask = define_task()
    selected_machines_sequential = []

    iter_sequantial = iter(sorted_list_of_configuration_machine_sequential)
    current_cost_of_execution_sequential_tasks_in_current_machine = math.inf
    # нужно поробовать пересчиать на одной машине, на двух и до бесконечности

    try:
        while current_cost_of_execution_sequential_tasks_in_current_machine > common_price_for_all_sequentuial_tasks:
            current_machine_configuration = next(iter_sequantial)
            selected_machines_sequential = [current_machine_configuration]
            switch = ConfigurationOfSwitches(1)
            machine = ConfigurationOfMachines(1, current_machine_configuration[1],
                                              current_machine_configuration[0])
            for i in range(len(descriptionOffTask)):
                current_task = descriptionOffTask.iloc[i]
                current_cost_of_execution_sequential_tasks_in_current_machine += (machine.working_time_with_particular_task(
                    current_task, current_task["complexityOfTask"]) + switch.calculate_transfer_time_from(1, current_task) + switch.calculate_transfer_time_to(1, current_task)) * machine.price + switch.calculate_transfer_price(1,current_task)\


    except StopIteration:
        selected_machines_sequential = [sorted_list_of_configuration_machine_sequential[-1]]


        return selected_machines_sequential





def greedy_algorithm_for_configuration_of_machine(CPU, coreFreq, price_limit):

    # список машин для параллельного вычисления
    sorted_list_of_configuration_machine_parallel = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
    sorted_list_of_configuration_machine_parallel = sorted(list(itertools.chain(*sorted_list_of_configuration_machine_parallel)), reverse=True)

    # список машин для последовательного вычисления без распараллеливания
    sorted_list_of_configuration_machine_sequential = list(map(lambda x: list(zip([min(CPU)], [x])), coreFreq))
    sorted_list_of_configuration_machine_sequential = sorted(
        list(itertools.chain(*sorted_list_of_configuration_machine_sequential)), reverse=True)

    if max_number_of_sequential_machine < 2:
        selected_machines_sequential = analytical_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit)
    else:

        selected_machines_sequential = greedy_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit, max_number_of_sequential_machine)

    # remaining_price = price_limit

    selected_machines_parallel = []
    working_time = 0
    number_of_machine = 0
    cost_of_current_package = 0
    global working_time_of_current_package
    working_time_of_current_package = math.inf
    scheduling_table_of_current_package = pd.DataFrame()
    # for potential_machine in sorted_list_of_configuration_machine:
    itr = iter(sorted_list_of_configuration_machine_parallel)

    potential_machine = next(itr)
    taskGraph, descriptionOffTask = define_task()
    try:
        while True and number_of_machine < 16:
            # set current configuration of machine

            # configuartion for sequential machine

            machines_for_parallel, machines_for_sequential = from_list_machine_configuration(selected_machines_sequential, selected_machines_parallel)

            id_of_conf = len(selected_machines_parallel) + len(selected_machines_sequential)
            # id of machine, id of configuration, number of cpu
            machine = ConfigurationOfMachines(id_of_conf + 1, potential_machine[1], potential_machine[0])
            # print(potential_machine)
            machines_for_parallel.add_machine(machine)
            # print(selected_machines)

            common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines_for_sequential, machines_for_parallel)
            price_of_all_working = sum(scheduling_table["executingPrice"]) + sum(scheduling_table["transferPrice"])
            # print(scheduling_table)
            # print(price_of_all_working, selected_machines_parallel, potential_machine)
            # print(sum(scheduling_table[scheduling_table["possibilityOfParalleling"] > 0.3]["transferTime"]), sum(scheduling_table[scheduling_table["possibilityOfParalleling"] > 0.3]["executingTime"]))
            if price_of_all_working < price_limit and sum(scheduling_table[scheduling_table["possibilityOfParalleling"] > 0.3]["transferTime"]) < sum(scheduling_table[scheduling_table["possibilityOfParalleling"] > 0.3]["executingTime"]): # добавим ограничение время на тарнсфер бменьше времени на выполнение
                selected_machines_parallel.append(potential_machine)
                number_of_machine = len(selected_machines_parallel) + 1
                cost_of_current_package = price_of_all_working
                working_time_of_current_package = common_time
                scheduling_table_of_current_package = scheduling_table
                class_machines_parallel = machines_for_parallel
                itr = iter(sorted_list_of_configuration_machine_parallel)
                potential_machine = next(itr)
            else:
                potential_machine = next(itr)

        if working_time_of_current_package > 0:
            print("selected_machines", selected_machines_sequential, selected_machines_parallel)
            print("price_of_all_working", cost_of_current_package)
            print("working_time_of_best_package", working_time_of_current_package)

    except StopIteration:
        print("selected_machines", selected_machines_sequential, selected_machines_parallel)
        print("price_of_all_working", cost_of_current_package)
        print("working_time_of_best_package", working_time_of_current_package)
        print(number_of_machine)
        if working_time_of_current_package == math.inf:
            print("!Increase the price-limit or simplify the task!")
            raise ValueError("Increase the price-limit or simplify the task")
        scheduling_table_of_current_package = scheduling_table_of_current_package.sort_values(by="indexOfTask")
        scheduling_table_of_current_package = transform_table_with_true_start_end_time(scheduling_table_of_current_package)
    finally:
        del itr

    return selected_machines_sequential, selected_machines_parallel, cost_of_current_package, working_time_of_current_package, scheduling_table_of_current_package, class_machines_parallel




CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 16500


selected_machines_sequential_greedy, selected_machines_parallel_greedy, cost_of_current_package, working_time_of_current_package, scheduling_table_of_current_package, class_machines_parallel_greedy = greedy_algorithm_for_configuration_of_machine(CPU, coreFreq, price_limit)





# print(greedy_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit, max_number_of_sequential_machine))
# from evaluating of effectiveness of working of greedy algorithms xl <= x* <=2xl
# where xl - results of working greedy algorithm
