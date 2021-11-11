from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *
import pandas as pd
import numpy as np
import random
import math
from deap import base
from deap import creator
from deap import tools
from deap import algorithms


max_number_of_machine = 16
CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
global price_limit
price_limit = 14000

number_of_task = list(range(1, max_number_of_machine + 1))

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              reverse=True)

length_of_variation = len(sorted_list_of_configuration_machine)  # length of individuals
# example of initial sample. can be thinking about it. the value is numbers of taken machines


def calculate_time_and_price_of_current_set_of_machines(sample_of_machines):
    sample_of_machines = sample_of_machines[1:]
    lenght_of_variation = sum(sample_of_machines[1:])


    if lenght_of_variation < 1:
        return math.inf, math.inf

    taskGraph, descriptionOffTask = define_task()

    machines_for_parallel = SetOfMachines(lenght_of_variation)
    switch_parallel = ConfigurationOfSwitches(lenght_of_variation)
    sample_parallel = sample_of_machines[1:]

    # for sequential tasks
    sample_sequential = [(2, 1)]
    pricesOfUsingMachines = {}
    machines_for_sequential = SetOfMachines(1)
    switch_sequential = ConfigurationOfSwitches(1)

    machine = ConfigurationOfMachines(1, sample_sequential[0][1], sample_sequential[0][0])
    machines_for_sequential.add_machine(machine)
    machines_for_sequential.add_switch(switch_sequential)
    pricesOfUsingMachines[machine.id] = machine.price
    # print(number_of_machine)



    '''
    sequential_machine = sample_of_machines[0]
    machines_for_sequential = SetOfMachines(1)
    switch_sequential = ConfigurationOfSwitches(1)

    machine = ConfigurationOfMachines(1, sorted_list_of_configuration_machine[sequential_machine-1][1],
                                      sorted_list_of_configuration_machine[sequential_machine-1][0])
    machines_for_sequential.add_machine(machine)
    machines_for_sequential.add_switch(switch_sequential)
    pricesOfUsingMachines[machine.id] = machine.price
    # print(number_of_machine)


    sample_parallel = sample_of_machines[1:]
    machines_for_parallel = SetOfMachines(lenght_of_variation - 1)
    switch_parallel = ConfigurationOfSwitches(lenght_of_variation)
    '''



    id_of_machine = 2
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
    price_of_all_working = sum(scheduling_table.apply(
        find_common_price, axis=1, pricesOfUsingMachines=pricesOfUsingMachines)) + sum(
        scheduling_table["transferPrice"])

    return common_time, price_of_all_working


def evaluate(individual):
    individual = individual[0]
    common_time, price_of_all_working = calculate_time_and_price_of_current_set_of_machines(individual)
    if price_of_all_working > price_limit:
        return math.inf,
    elif sum(individual) > 16 or individual[0] > 16:
        return math.inf,
    else:
        return common_time,


def n_per_product():
    #rng = np.random.default_rng()
    #sample_sequential = rng.multinomial(1, [1 / 16] * 16, size=1)

    sequential_machine = np.random.randint(1, 16)
    summa = np.random.randint(1, 15)
    rng = np.random.default_rng()
    sample_parallel = rng.multinomial(summa, [1 / 15] * 15, size=1)

    return np.append(sequential_machine, sample_parallel).tolist()

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

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # create class FitnessMin, the weights = -1 means that fitness - is function for minimum
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("n_per_product", n_per_product)  # generation function
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.n_per_product, n=1200)  # create from n_per_product fucntion one individual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
hof = tools.HallOfFame(5)

toolbox.decorate("mate", checkBounds(0, 16))
toolbox.decorate("mutate", checkBounds(0, 16))

pop = toolbox.population(n=300)  # создаем популяцию размером 300 из 100 различных индивидов
# Evaluate the entire population


fitnesses = list(map(toolbox.evaluate, pop))  # map to each individual fitness function

for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
    CXPB, MUTPB = 0.8, 0.3
fits = [ind.fitness.values[0] for ind in pop]

# save best individuals
hof = tools.HallOfFame(5)

g = 0

# 30 - is number of generations
while g < 30:
    g = g + 1
    print("-- Generation %i --" % g)

    # select individuals
    offspring = toolbox.select(pop, len(pop))

    # clone selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # take 2 individual's as input 1 modified individuals
    for child1, child2 in zip(offspring[::2], offspring[1::2]): # берем через 1: (1,3,5) и (2,4,6) и получаем  пары 1,2;3,4; 5,6
        if random.random() < CXPB: # из получившегося списка
            toolbox.mate(child1[0], child2[0]) # crossover
            del child1.fitness.values
            del child2.fitness.values
    # take 1 individuals as input and return 1 individuals as output
    # мутация
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant[0])
            del mutant.fitness.values

    # Gather all the fitnesses in one list and print the stats
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    # для каждого индивида - оценка
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit


    # renewing population

    pop[:] = offspring
    hof.update(pop)

    fits = [ind.fitness.values[0] for ind in pop]

    print()
    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5

    best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
    print(evaluate(best))

# best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
best = hof[0]
best_fit = hof[0].fitness

print(evaluate(best))
print(best[0])
print(calculate_time_and_price_of_current_set_of_machines(best[0]))

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
