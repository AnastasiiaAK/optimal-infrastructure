'''
Можно подумать, что задачи могут быть нескольких типов, в зависимости от этого нужно максимизировать разные элементы конфигурации:
1. Сложные по вычислению задачи. для них нужно максимально мощные машины
2. Большие по памяти задачи, для них нужны лучшие свитчи
Подумаем, как лучше определить тип задачи
'''


from sequential_modification.setTaskSequential import *
from sequential_modification.find_optimal_minimum_and_maximum_numbers_of_machine import *

# рассмотрим данные
# если время передачи на самых слабых машинах больше, чем время выполнения, то считаем эту задачу memory intensive

list_min_seq = [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)]
list_min_parallel = [(2, 1)]


def transfer_execution_time(list_min_seq, list_min_parallel):
    taskGraph, descriptionOffTask = define_task()
    machines_for_parallel, machines_for_sequential = from_list_machine_configuration(list_min_seq, list_min_parallel)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask,
                                                                   machines_for_sequential, machines_for_parallel)
    # print(common_time)
    sequential_table = scheduling_table[scheduling_table["possibilityOfParalleling"] < 0.3]
    transfer_time_seq = sum(sequential_table["executingTimeWithTransfer"]) - sum(sequential_table["executingTimeWithoutTransfer"])
    execution_time_seq = sum(sequential_table["executingTimeWithoutTransfer"])
    parallel_table = scheduling_table[scheduling_table["possibilityOfParalleling"] >= 0.3]
    transfer_time_par = sum(parallel_table["executingTimeWithTransfer"]) - sum(parallel_table["executingTimeWithoutTransfer"])
    execution_time_par = sum(parallel_table["executingTimeWithoutTransfer"])
    common_transfer_time = transfer_time_seq + transfer_time_par
    common_execution_time = execution_time_seq + execution_time_par


    return common_transfer_time, common_execution_time


common_transfer_time, common_execution_time = transfer_execution_time(list_min_seq, list_min_parallel)

type_of_task = 0
if common_transfer_time <= common_execution_time:
    type_of_task = "complexity"
else:
    type_of_task = "memory"


print(type_of_task)
'''

что делать с мемори интеенсив и когда добавлять свитч

- для комплексити интенсив - добавляем свитч, когда достигли максимальной цены по машинам
- для мемори  интенсив - добавляем минмиальыне машины и затем меняем свитч пока, не закончаться деньги или пока время передачи не станет меньше времени выполнения
если стала меньше рвемен выполненитя - пытаемся добавить более сложные машины, псле этого опять проверяем не стало ли время передачи больше временги выполненитя
'''

