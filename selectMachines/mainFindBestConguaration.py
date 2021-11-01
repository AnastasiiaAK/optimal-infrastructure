# задаем параметры CPUOfTask, memoryOfTask, budgetLimit, numberOfTask in workflow
import math

from selectMachines.findNumberOfMachine import *


if __name__ == '__main__':
    CPUOFTask = 100
    memoryOfTask = 100
    budgetLimit = 1000
    numberOfMachines, bestTimeForNumberOfMachines, bestConfiguration = findNumberOfMachine(CPUOFTask, memoryOfTask, budgetLimit, G)
    print(numberOfMachines, bestTimeForNumberOfMachines, bestConfiguration)

# print(f"Best results algorithm shows in {numberOfMachines} machines with following configuration/
# CPU = {bestConfiguration[0]}, memoryBest = {bestConfiguration[1]}. Common time = {bestTimeForNumberOfMachines}")
