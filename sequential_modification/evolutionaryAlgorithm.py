from sequential_modification.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, proportion_of_price_for_different_type_of_tasks, find_common_price, transform_table_with_true_start_end_time
import itertools
from sequential_modification.algorithmOfParalleltask import *
import pandas as pd
import numpy as np
import random
import math
from deap import base
from deap import creator
from deap import tools
from deap import algorithms


CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
global price_limit
price_limit = 37000

global sample_sequential_init
# sample_sequential_init = analytical_algorithm_for_sequential_tasks(CPU, coreFreq, price_limit)

common_price_for_all_sequential_tasks, common_price_for_all_parallel_tasks = proportion_of_price_for_different_type_of_tasks(
        price_limit, proportion_of_parallel_tasks, proportion_of_sequential_tasks)
print(common_price_for_all_sequential_tasks, common_price_for_all_parallel_tasks )
sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))


sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              reverse=True)
sorted_list_of_configuration_machine_sequential = list(map(lambda x: list(zip([min(CPU)], [x])), coreFreq))
sorted_list_of_configuration_machine_sequential = sorted(
        list(itertools.chain(*sorted_list_of_configuration_machine_sequential)), reverse=True)

length_of_variation = len(sorted_list_of_configuration_machine)  # length of individuals
# example of initial sample. can be thinking about it. the value is numbers of taken machinesf


def calculate_time_and_price_of_current_set_of_machines(sample_of_machines):
    lenght_of_variation = sum(sample_of_machines[0])
    # print(sample_of_machines)
    # print(lenght_of_variation)
    if lenght_of_variation < 1:
        return math.inf, math.inf


    taskGraph, descriptionOffTask = define_task()

    machines_for_parallel = SetOfMachines(lenght_of_variation)
    switch_parallel = ConfigurationOfSwitches(lenght_of_variation)
    sample_parallel = sample_of_machines[0]

    # for sequential tasks
    sample_sequential = sample_sequential_init
    pricesOfUsingMachines = {}
    machines_for_sequential = SetOfMachines(len(sample_sequential))
    switch_sequential = ConfigurationOfSwitches(1)

    for id, seq_machine in enumerate(sample_sequential):
        machine = ConfigurationOfMachines(id + 1, seq_machine[1], seq_machine[0])
        machines_for_sequential.add_machine(machine)
        pricesOfUsingMachines[machine.id] = machine.price

    machines_for_sequential.add_switch(switch_sequential)

    # print(number_of_machine)
    id_of_machine = len(sample_sequential) + 1
    for i, numbers_of_machines in enumerate(sample_parallel):
        for _ in range(numbers_of_machines):
            machine = ConfigurationOfMachines(id_of_machine, sorted_list_of_configuration_machine[i][1], sorted_list_of_configuration_machine[i][0])
            machines_for_parallel.add_machine(machine)
            pricesOfUsingMachines[machine.id] = machine.price
            id_of_machine += 1
    machines_for_parallel.add_switch(switch_parallel)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines_for_sequential, machines_for_parallel)
    price_of_all_working = sum(scheduling_table.apply(
        find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
        scheduling_table["transferPrice"])
    price_of_all_working = sum(scheduling_table["executingPrice"]) + sum(scheduling_table["transferPrice"])
    return common_time, price_of_all_working

# print("kii", calculate_time_and_price_of_current_set_of_machines([[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0]]))


def calculate_time_and_price_of_current_set_of_sequential_machines(sample_of_machines):
    pricesOfUsingMachines = {}
    common_number_of_machine = sum(sample_of_machines[0])
    if common_number_of_machine == 0:
        return math.inf, math.inf

    machines_for_sequential = SetOfMachines(6)
    switch_sequential = ConfigurationOfSwitches(4)  # посмотреть
    sample_sequential = sample_of_machines[0]
    machines_for_sequential.add_switch(switch_sequential)

    taskGraph, descriptionOffTask = define_task()

    id_of_machine = 1
    for i, numbers_of_machines in enumerate(sample_sequential):
        for _ in range(numbers_of_machines):
            machine = ConfigurationOfMachines(id_of_machine, sorted_list_of_configuration_machine_sequential[i][1], sorted_list_of_configuration_machine_sequential[i][0])
            machines_for_sequential.add_machine(machine)
            pricesOfUsingMachines[machine.id] = machine.price
            id_of_machine += 1

    # for parallel tasks
    machines_for_parallel = SetOfMachines(1)
    switch_parallel = ConfigurationOfSwitches(1)
    machine = ConfigurationOfMachines(common_number_of_machine + 1, 1, 4)
    pricesOfUsingMachines[machine.id] = machine.price
    machines_for_parallel.add_machine(machine)
    machines_for_parallel.add_switch(switch_parallel)

    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask,
                                                                   machines_for_sequential, machines_for_parallel)
    scheduling_table = scheduling_table[scheduling_table["possibilityOfParalleling"] < 0.3]

    price_of_all_working = sum(scheduling_table["executingPrice"]) + sum(scheduling_table["transferPrice"])
    common_time = common_time

    return common_time, price_of_all_working


def evaluate(individual):
    individual = individual[0]
    common_time, price_of_all_working = calculate_time_and_price_of_current_set_of_machines(individual)
    if price_of_all_working > price_limit:
        return math.inf,
    elif sum(individual[0]) > 16:
        return math.inf,
    else:

        return common_time,


def evaluate_sequential(individual):
    individual = individual[0]
    common_time, price_of_all_working = calculate_time_and_price_of_current_set_of_sequential_machines(individual)
    if price_of_all_working > common_price_for_all_sequential_tasks:
        return math.inf,
    elif sum(individual[0]) != 6 or sum(individual[0]) < 1:
        return math.inf,
    else:
        return common_time,


def n_per_product_seq(max_number_of_machine, max_possible_configuration):
    #rng = np.random.default_rng()
    #sample_sequential = rng.multinomial(1, [1 / 16] * 16, size=1)
    sequential_machine = np.random.randint(1, 7)
    summa = max_number_of_machine
    rng = np.random.default_rng()
    sample_parallel = rng.multinomial(summa, [1 / 4] * 4, size=1)

    return sample_parallel.tolist()


def n_per_product_par(max_number_of_machine, max_possible_configuration):
    # rng = np.random.default_rng()
    # sample_sequential = rng.multinomial(1, [1 / 16] * 16, size=1)
    sequential_machine = np.random.randint(1, max_number_of_machine + 1)
    summa = np.random.randint(1, max_number_of_machine + 1)
    rng = np.random.default_rng()
    sample_parallel = rng.multinomial(summa, [1 / max_possible_configuration] * max_possible_configuration, size=1)
    return sample_parallel.tolist()



def checkBounds(min, max):
    def decorator(func):
        def wrappper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrappper
    return decorator


def evolution_algorithm_for_parallel_tasks(max_number_of_machine, max_possible_configuration, evaluate, number_of_generation, size_of_population, n_per_product, CXPB=0.8, MUTPB=0.2):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # create class FitnessMin, the weights = -1 means that fitness - is function for minimum
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("n_per_product", n_per_product, max_number_of_machine=max_number_of_machine, max_possible_configuration=max_possible_configuration)  # generation function
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.n_per_product, n=5000)  # create from n_per_product fucntion one individual
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=4)
    hof = tools.HallOfFame(5)
    toolbox.decorate("mate", checkBounds(0, max_number_of_machine))
    toolbox.decorate("mutate", checkBounds(0, max_number_of_machine))
    pop = toolbox.population(n=size_of_population)  # создаем популяцию размером 300 из 100 различных индивидов
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))  # map to each individual fitness function
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        CXPB, MUTPB = 0.8, 0.3
    fits = [ind.fitness.values[0] for ind in pop]
    # save best individuals
    hof = tools.HallOfFame(5)
    list_of_hof = []
    g = 0
    # 30 - is number of generations
    while g < number_of_generation:
        g = g + 1
        # pop.append(list_of_hof)
        if g > 15:
            MUTPB = 0.5
        elif g > 30:
            MUTPB = 0.7
        print("-- Generation %i --" % g)
        if hof is not None:
            hof.update(pop)
        # select individuals
        offspring = toolbox.select(pop, len(pop))
        # clone selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # take 2 individual's as input 1 modified individuals
        for child1, child2 in zip(offspring[::2], offspring[1::2]): # берем через 1: (1,3,5) и (2,4,6) и получаем  пары 1,2;3,4; 5,6
            if random.random() < CXPB: # из получившегося списка
                toolbox.mate(child1[0][0], child2[0][0]) # crossover
                del child1.fitness.values
                del child2.fitness.values
        # take 1 individuals as input and return 1 individuals as output
        # мутация
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant[0][0])
                del mutant.fitness.values
        # Gather all the fitnesses in one list and print the stats
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # для каждого индивида - оценка
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if hof is not None:
            hof.update(offspring)
        # renewing population
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        print()
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5
        best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
        print(evaluate(best))
        list_of_hof.append(hof)
    # best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
    best = hof[0]
    best_fit = hof[0].fitness
    print(evaluate(best))
    print(best[0])
    print(best_fit)
    return best[0], best_fit


def count_machine_in_sorted_list_to_list_of_configurations(sequential_set):
    sample_sequential_init = []
    for index, i in enumerate(sequential_set[0]):
        count = 0
        while count < i:
            sample_sequential_init.append((sorted_list_of_configuration_machine_sequential[index][0], sorted_list_of_configuration_machine_sequential[index][1]))
            count += 1
    return sample_sequential_init


# sample_sequential_init = [(2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4)]
# par_m = [[0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# print("44444")
# print(calculate_time_and_price_of_current_set_of_sequential_machines([[6,0,0,0]]))
# print(calculate_time_and_price_of_current_set_of_machines(par_m))

max_number_of_machine = 6
if max_number_of_machine > 1:
    sequential_set, best_fit = evolution_algorithm_for_parallel_tasks(max_number_of_machine, len(sorted_list_of_configuration_machine_sequential), evaluate_sequential , 2, 25, n_per_product_seq) # max_number_of_machine, max_possible_configuration, evaluate, number_of_generation, size_of_population, maximum_values_of_machine
    print(sequential_set, best_fit)
    sample_sequential_init = count_machine_in_sorted_list_to_list_of_configurations(sequential_set)

    if best_fit.values[0] == math.inf:
        sequential_set = [0, 0, 0, 6]
        sample_sequential_init = count_machine_in_sorted_list_to_list_of_configurations(sequential_set)

print("sample_sequential_init", sample_sequential_init)

del creator.FitnessMin
del creator.Individual

max_number_of_machine = 16




best_machine_evolution, _ = evolution_algorithm_for_parallel_tasks(16, len(sorted_list_of_configuration_machine), evaluate, 2, 50, n_per_product_par) # max_number_of_machine, max_possible_configuration, evaluate, number_of_generation, size_of_population



def calculate_time_and_price_of_current_set_of_machines1(sample_of_machines):
    lenght_of_variation = sum(sample_of_machines[0])
    # print(sample_of_machines)
    # print(lenght_of_variation)
    if lenght_of_variation < 1:
        return math.inf, math.inf
    taskGraph, descriptionOffTask = define_task()

    machines_for_parallel = SetOfMachines(lenght_of_variation)
    switch_parallel = ConfigurationOfSwitches(lenght_of_variation)
    sample_parallel = sample_of_machines[0]

    # for sequential tasks
    sample_sequential = sample_sequential_init
    pricesOfUsingMachines = {}
    machines_for_sequential = SetOfMachines(len(sample_sequential))
    switch_sequential = ConfigurationOfSwitches(1)

    for id, seq_machine in enumerate(sample_sequential):
        machine = ConfigurationOfMachines(id + 1, seq_machine[1], seq_machine[0])
        machines_for_sequential.add_machine(machine)
        pricesOfUsingMachines[machine.id] = machine.price

    machines_for_sequential.add_switch(switch_sequential)
    # print(number_of_machine)
    id_of_machine = len(sample_sequential) + 1
    for i, numbers_of_machines in enumerate(sample_parallel):
        for _ in range(numbers_of_machines):
            # print(id_of_machine)
            machine = ConfigurationOfMachines(id_of_machine, sorted_list_of_configuration_machine[i][1], sorted_list_of_configuration_machine[i][0])
            machines_for_parallel.add_machine(machine)
            pricesOfUsingMachines[machine.id] = machine.price
            id_of_machine += 1
    machines_for_parallel.add_switch(switch_parallel)
    # print(selected_machines)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines_for_sequential, machines_for_parallel)

    price_of_all_working = sum(scheduling_table["executingPrice"]) + sum(scheduling_table["transferPrice"])
    return common_time, price_of_all_working, machines_for_parallel, scheduling_table


_, _, machines_for_parallel_evolution, res_table_evolution = calculate_time_and_price_of_current_set_of_machines1(best_machine_evolution)
res_table_evolution = transform_table_with_true_start_end_time(res_table_evolution)

'''
Steps
1. initial population
2. measure fitness of individual
3. repeat under convergence:
3.1 choose representatives of the population for reproduction
3.2 spawn new individuals by crossing and mutation
3.3 measure fitness of got child
3.4 replace the least fit individuals to child
'''
