import pandas as pd
from sequential_modification.greedyAlgorithm import scheduling_table_of_current_package, class_machines_parallel_greedy, selected_machines_sequential_greedy, selected_machines_parallel_greedy
from sequential_modification.evolutionaryAlgorithm import res_table_evolution, machines_for_parallel_evolution, best_machine_evolution, sorted_list_of_configuration_machine, sample_sequential_init
from sequential_modification.parameters import dictFreq, dictSwitches

# executingTimeWithTransfer inclusing transfer time from previous machine to current and from current machine to next
# priceOfAllWork = executingTimeWithTransfer * priceOfUsingMachine + priceOfUsingTransfer

total_information = ["Total price for all work", "Total time for all work",
                     "Total transfer time", "Total transfer price",
                     "Total execution time", "Total execution price"]

table_columns = ["Task price for all work", "Task time for all work",
                 "Task transfer time", "Task transfer price",
                 "Task execution time", "Time for I", "Time for O", "Task execution price",
                 "Incoming memory", "Outgoing memory",
                 "Information about each working machine for tasks (what part is performs, how much memory, what time, what price)"]

greedy_table = scheduling_table_of_current_package

# _, _, evolut_table = evolution_algorithm_for_parallel_tasks(16, len(sorted_list_of_configuration_machine), evaluate, 50, 500) #max_number_of_machine, max_possible_configuration, evaluate, number_of_generation, size_of_population,
sorted_list_of_configuration_machine
best_machine_evolution1 = []
for i, count in enumerate(best_machine_evolution[0]):
    if count != 0:
        c = 0
        while c < count:
            best_machine_evolution1.append(sorted_list_of_configuration_machine[i])
            c += 1
best_machine_evolution = best_machine_evolution1


'''
common_time, price_of_all_working, evolution_table = calculate_time_and_price_of_current_set_of_machines(
    [[0, 0, 0, 1, 0, 2, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
'''


def define_configuration(task, list_of_sequential_machine, list_of_parallel_machine):

    if float(task["possibilityOfParalleling"]) < 0.3:
        return list_of_sequential_machine[task["idOfMachine"]-1]
    else:
        list_conf = []
        for id in task["idOfMachine"]:
            conf = list_of_parallel_machine[id - 1 - len(list_of_sequential_machine)]
            list_conf.append(conf)
        return list_conf


def define_switch(task):
    try:
        numb_of_machine = len(task["idOfMachine"])
        if numb_of_machine <= 4:
            id_of_swithes = 1
        elif numb_of_machine > 8:
            id_of_swithes = 3
        else:
            id_of_swithes = 2
    except:
        return dictSwitches[1]["frequency"]
    return dictSwitches[id_of_swithes]["frequency"]


def calculating_common_time(scheduling_table_of_current_package):
    common_time = 0
    list_of_priority = scheduling_table_of_current_package["priority"].unique()
    for prior in list_of_priority:
        max_time_in_current_priority = scheduling_table_of_current_package[scheduling_table_of_current_package["priority"] == prior]["executingTime"].max()
        common_time += max_time_in_current_priority

    return common_time

def print_information_for_table_received_by_some_alg(result_table, machine_parallel, list_of_sequential_machine, list_of_parallel_machine):
    # for overall tasks
    total_price_for_all_work = sum(result_table["transferPrice"]) + sum(
        result_table["executingPrice"])  # total task completion time


    total_time_for_all_work = calculating_common_time(result_table)  # total cost of completing task

    total_transfer_time = sum(result_table["executingTimeWithTransfer"]) - sum(result_table["executingTimeWithoutTransfer"])  # total transfer time
    total_execution_time_with_transfer = sum(
        result_table["executingTimeWithTransfer"])  # total time of working machine (with tarnsfer from both side)
    total_execution_time_without_transfer = sum(result_table["executingTimeWithoutTransfer"])  # time of executing task


    total_transfer_price = sum(result_table["transferPrice"])  # total transfer price

    total_price_for_execution = sum(result_table["executingPrice"])  # cost of execution without transfer
    set_of_sequential_machine = list_of_sequential_machine
    set_of_parallel_machine = list_of_parallel_machine

    print(f"{total_price_for_all_work=}\n"
          f"{total_time_for_all_work=}\n",
          ("Следующие параметры рассчитаны как сумма времени выполнения задач (без учета того, что некоторые выполняются одновременно (параллельно)"),

          f"{total_transfer_time=}\n"
          f"{total_transfer_price=}\n"
          f"{total_execution_time_with_transfer=}\n"
          f"{total_execution_time_without_transfer=}\n"
          f"{total_price_for_execution=}\n"
          f"{set_of_sequential_machine}\n"
          f"{set_of_parallel_machine}\n")

    # for each task separately
    result_table["transfer_Input"] = result_table["transferTime"]
    result_table["transfer_Output"] = result_table["transfer_Input"].shift(periods=-1, fill_value=0)

    result_table["configuration_of_current_machine(number_of_CPU, frequency)"] = result_table[["possibilityOfParalleling", "idOfMachine"]].apply(define_configuration, args=(list_of_sequential_machine, list_of_parallel_machine),  axis=1)
    result_table["configuration_of_current_switches(frequency)"] = result_table.apply(define_switch, axis=1)

    change_type = result_table.drop(['done', 'idOfMachine', "configuration_of_current_machine(number_of_CPU, frequency)"], axis=1)
    change_type = change_type.astype("float64")
    change_type = change_type.round(2)

    change_type[["done", "idOfMachine",  "configuration_of_current_machine(number_of_CPU, frequency)", "configuration_of_current_switches(frequency)"]] = result_table[["done", "idOfMachine", "configuration_of_current_machine(number_of_CPU, frequency)", "configuration_of_current_switches(frequency)"]]

    result_table = change_type[['indexOfTask', "nameOfTask", "complexityOfTask",
                                "complexityPerUnitOfmemory", "incomingMemory",
                                "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                'configuration_of_current_machine(number_of_CPU, frequency)',
                                'configuration_of_current_switches(frequency)',
                                "startTime", "endTime", "executingTimeWithoutTransfer",
                                "executingTimeWithTransfer", "executingPrice",
                                "transfer_Input", "transfer_Output", "transferPrice", "done"]]



    result_table = change_type[['indexOfTask', "nameOfTask", "complexityOfTask",
                                 "incomingMemory", "outgoingMemory", "possibilityOfParalleling",
                                'configuration_of_current_machine(number_of_CPU, frequency)',
                                'configuration_of_current_switches(frequency)', "executingTimeWithoutTransfer",
                                "executingTimeWithTransfer", "executingPrice", "transferPrice",
                                "transfer_Input", "transfer_Output", "done"]]

    del change_type

    # for each machine in parallel tasks

    id_of_parallel_tasks = result_table[result_table["possibilityOfParalleling"] > 0.3]["indexOfTask"].values

    # create for each parallel task - dataframe
    # Information about each working machine for tasks (what part is performs, how much memory, what time, what price)
    for task_id in id_of_parallel_tasks:

        task = result_table[result_table["indexOfTask"] == task_id]
        d = {}
        common_cpu = 0
        list_id_of_machines = []
        for i in machine_parallel.listOfMachines:
            common_cpu += i.CPU * i.core_freq
            list_id_of_machines.append(i.id)

        for machine in machine_parallel.listOfMachines:
            d[machine.id] = {}
            d[machine.id]["part_of_task"] = float(machine.CPU * machine.core_freq / common_cpu)
            d[machine.id]["part_of_complexity"] = float(machine.CPU * machine.core_freq / common_cpu) * float(
                task["complexityOfTask"].values)
            d[machine.id]["part_of_memory"] = machine.CPU * machine.core_freq / common_cpu * task[
                "incomingMemory"].values
            d[machine.id]["part_of_memory"] = machine.CPU * machine.core_freq / common_cpu * task[
                "incomingMemory"].values
            d[machine.id]["time_of_work"] = machine.working_time_with_particular_task(task,
                                                                                      machine.CPU * machine.core_freq
                                                                                      / common_cpu *
                                                                                      task["complexityOfTask"].values)
            d[machine.id]["price_of_work"] = d[machine.id]["time_of_work"] * machine.price
            d[machine.id]["machine_configuration(number_of_CPU, frequency)"] = (machine.CPU, machine.core_freq)


        a = pd.DataFrame.from_dict(d, orient='index')

        globals()['information_about_operation_of_machine_in_task_{0}'.format(int(task_id))] = a


    # print(information_about_operation_of_machine_in_task_4)
    # print information about using machines in each parallel tasks

    return result_table, information_about_operation_of_machine_in_task_4


# for greedy
print("information about results of working of greedy algorithm")
greedy_result, greedy_for_each_parallel_tasks = print_information_for_table_received_by_some_alg(greedy_table, class_machines_parallel_greedy, selected_machines_sequential_greedy, selected_machines_parallel_greedy)

# for evolution
print("information about results of working of evolution algorithm")
evolution_result, evolution_for_each_parallel_tasks = print_information_for_table_received_by_some_alg(res_table_evolution, machines_for_parallel_evolution, sample_sequential_init, best_machine_evolution)

