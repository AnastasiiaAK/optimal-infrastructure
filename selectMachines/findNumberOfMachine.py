# задаем параметры CPUOfTask, memoryOfTask, budgetLimit, numberOfTask in Graph


from selectMachines.selectConfigurationOfMachine import *
'''
def findNumberOfMachine(CPUOfTask, memoryOfTask, budgetLimit, numberOfTask):

    G = generateTask(numberOfTask)
    import math
    numberOfMachines = 1
    bestTimeForNumberOfMachines = math.inf
    currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines, CPUOfTask, memoryOfTask, G)
    currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]
    while currentBestConfForNumberOfMachines[4] < budgetLimit and (numberOfMachines * memoryOfTask / 50) < bestTimeForNumberOfMachines and currentBestTimeForNumberOfMachines < bestTimeForNumberOfMachines:
        #currentBestTimeForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines)[3]

        if  currentBestTimeForNumberOfMachines < bestTimeForNumberOfMachines:
            bestTimeForNumberOfMachines = currentBestTimeForNumberOfMachines
            bestConfiguration = currentBestConfForNumberOfMachines


        currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines+1, CPUOfTask, memoryOfTask, G)

        currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]
        numberOfMachines += 1
    print("optimal number of machines", numberOfMachines,'', "best Time For Number Of Machines", bestTimeForNumberOfMachines)
    return numberOfMachines, bestTimeForNumberOfMachines, bestConfiguration


def findNumberOfMachine(CPUOfTask, memoryOfTask, budgetLimit, G):

    import math
    numberOfMachines = 1
    bestTimeForNumberOfMachines = math.inf
    currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines, CPUOfTask, memoryOfTask, G)
    currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]


    while currentBestConfForNumberOfMachines[4] < budgetLimit  and (numberOfMachines * memoryOfTask / 50) < bestTimeForNumberOfMachines and currentBestTimeForNumberOfMachines < bestTimeForNumberOfMachines:
        #currentBestTimeForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines)[3]

        if  currentBestTimeForNumberOfMachines < bestTimeForNumberOfMachines:
            bestTimeForNumberOfMachines = currentBestTimeForNumberOfMachines
            bestConfiguration = currentBestConfForNumberOfMachines

        currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines+1, CPUOfTask, memoryOfTask, G)
        currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]
        numberOfMachines += 1
    print("optimal number of machines", numberOfMachines,'', "best Time For Number Of Machines", bestTimeForNumberOfMachines)
    return numberOfMachines, bestTimeForNumberOfMachines, bestConfiguration
'''


def findNumberOfMachine(CPUOfTask, memoryOfTask, budgetLimit, G):
    import math
    numberOfMachines = 1
    bestTimeForNumberOfMachines = math.inf
    currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines, CPUOfTask, memoryOfTask, G)

    if currentBestConfForNumberOfMachines == -1:
        print("увеличьте бюджет или упростите конфигурацию")
        return None, None, None

    currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]

    while True and currentBestConfForNumberOfMachines[4] < budgetLimit and (
            numberOfMachines * memoryOfTask / 50) < bestTimeForNumberOfMachines:
        # currentBestTimeForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines)[3]

        if currentBestTimeForNumberOfMachines < bestTimeForNumberOfMachines:
            bestTimeForNumberOfMachines = currentBestTimeForNumberOfMachines
            bConfiguration = currentBestConfForNumberOfMachines
            bestNumberOfMachine = numberOfMachines

        currentBestConfForNumberOfMachines = bestConfuguration(budgetLimit, numberOfMachines + 1, CPUOfTask,
                                                               memoryOfTask, G)
        print(currentBestConfForNumberOfMachines)
        if currentBestConfForNumberOfMachines == -1:
            break
        currentBestTimeForNumberOfMachines = currentBestConfForNumberOfMachines[3]
        numberOfMachines += 1
    print("optimal number of machines", bestNumberOfMachine, '', "best Time For Number Of Machines",
          bestTimeForNumberOfMachines)
    return bestNumberOfMachine, bestTimeForNumberOfMachines, bConfiguration


