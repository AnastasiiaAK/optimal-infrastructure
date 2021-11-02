from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import define_task, find_common_price
import itertools
from newSelectMachinesWithHrZ.algorithmOfParalleltask import *

max_number_of_machine = 16
CPU = [2, 4, 8, 16]
coreFreqValues = [coreFreq1, coreFreq2, coreFreq3, coreFreq4]
coreFreq = [1, 2, 3, 4]
price_limit = 20000

number_of_task = list(range(1, max_number_of_machine + 1))

sorted_list_of_configuration_machine = list(map(lambda x: list(zip(CPU, [x] * len(CPU))), coreFreq))
sorted_list_of_configuration_machine = sorted(list(itertools.chain(*sorted_list_of_configuration_machine)),
                                              reverse=True)

number_of_machine = len(sorted_list_of_configuration_machine)  # length of individuals
# example of initial sample. can be thinking about it. 0 - not take i machines. 1 - take.
initial_sample = [0, 1, 0, 1, 0, 0, 0, 1, 0]

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
