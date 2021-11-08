from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *
import pandas as pd
import numpy as np
import random
from deap import base
from deap import creator
from deap import tools


max_number_of_machine = 16
CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
global price_limit
price_limit = 10000

number_of_task = list(range(1, max_number_of_machine + 1))

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              reverse=True)

length_of_variation = len(sorted_list_of_configuration_machine)  # length of individuals
# example of initial sample. can be thinking about it. the value is numbers of taken machines
initial_sample = [0, 1, 0, 1, 0, 0, 0, 1, 2]


def calculate_time_and_price_of_current_set_of_machines(sample_of_machines):
    lenght_of_variation = sum(sample_of_machines)

    pricesOfUsingMachines = {}
    machines = SetOfMachines(lenght_of_variation)
    switch = ConfigurationOfSwitches(lenght_of_variation)
    # print(number_of_machine)
    id_of_conf = 0
    taskGraph, descriptionOffTask = define_task()
    id_of_machine = 0

    for i, numbers_of_machines in enumerate(sample_of_machines):
        taskGraph, descriptionOffTask = define_task()
        for _ in range(numbers_of_machines):
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


def evaluate(individual):
    individual = individual[0][0]
    common_time, price_of_all_working = calculate_time_and_price_of_current_set_of_machines(individual)
    if price_of_all_working > price_limit:
        return 1000000000000000000000000000000000000000000000000000,
    elif sum(individual) > 16:
        return 1000000000000000000000000000000000000000000000000000,
    else:
        return common_time,


def n_per_product():
    summa = np.random.randint(1, 16)
    rng = np.random.default_rng()
    sample = rng.multinomial(summa, [1 / 16] * 16, size=1)
    return sample


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # create class FitnessMin, the weights = -1 means that fitness - is function for minimum
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("n_per_product", n_per_product)  # generation function
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.n_per_product, n=50)  # create from n_per_product fucntion one individual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


pop = toolbox.population(n=200)  # создаем популяцию размером 300 из 100 различных индивидов
# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, pop))  # map to each individual fitness function

for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
    CXPB, MUTPB = 0.5, 0.2
fits = [ind.fitness.values[0] for ind in pop]
g = 0
while g < 15:
    g = g + 1
    print("-- Generation %i --" % g)

    # select individuals
    offspring = toolbox.select(pop, len(pop))

    # clone selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # take 2 individual's as input 1 modified individuals
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1[0][0], child2[0][0])
            del child1.fitness.values
            del child2.fitness.values
    # take 1 individuals as input and return 1 individuals as output
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant[0][0])
            del mutant.fitness.values

    # Gather all the fitnesses in one list and print the stats
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    pop[:] = offspring

    fits = [ind.fitness.values[0] for ind in pop]
    print()
    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5

    best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
    print(evaluate(best))

best = pop[np.argmin([toolbox.evaluate(x) for x in pop])]
print(evaluate(best))
print(best[0])
print(calculate_time_and_price_of_current_set_of_machines(best[0][0]))
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
