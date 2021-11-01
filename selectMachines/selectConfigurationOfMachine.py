
from selectMachines.setParametersOfMachine import *
from selectMachines.calculateTimeInEachMachine import calculateTimeAndPrice
import math


def selectSeveralSuitableConfigaration(limitBudget, numberOfMachines, CPUOfTask, memoryOfTask, G):
    import math

    bestTime = math.inf
    suitableCPUForThisBudget = {}

    timeForTransferData = numberOfMachines * memoryOfTask / 50

    for i in range(len(CPU)):
        setOfAllMachines = setOfMachines(numberOfMachines)
        for resource in range(numberOfMachines):
            # считаем время и стоимость для минимальной конфигурации текущего CPU
            m1 = machine()
            m1.CPU = CPU[i]
            m1.memory = memory[0]
            m1.HDD = HDD[0]
            m1.availability = "free"
            m1.price = price[i] + memory[0] / 3000 + HDD[0] / 30000
            setOfAllMachines.addMachines(m1)

        timeForMinConf, budgetForMinConf = calculateTimeAndPrice(CPUOfTask, memoryOfTask, numberOfMachines,
                                                                 setOfAllMachines, G)
        # print(timeForMinConf, budgetForMinConf)

        setOfAllMachines = setOfMachines(numberOfMachines)

        # считаем время и стоимость для максимальной конфигурации текущего CPU
        for resource in range(numberOfMachines):
            m1 = machine()
            m1.CPU = CPU[i]
            m1.memory = memory[len(memory) - 1]
            m1.HDD = HDD[len(HDD) - 1]
            m1.availability = "free"
            m1.price = price[i] + memory[len(memory) - 1] / 3000 + HDD[len(HDD) - 1] / 30000
            setOfAllMachines.addMachines(m1)

        timeForMaxConf, budgetForMaxConf = calculateTimeAndPrice(CPUOfTask, memoryOfTask, numberOfMachines,
                                                                 setOfAllMachines, G)

        if limitBudget >= (budgetForMinConf):
            suitableCPUForThisBudget[i] = [timeForMinConf, timeForMaxConf]
    return suitableCPUForThisBudget


def findMinimumTimeFromSuitableMachines(suitableCPUForThisBudget):
    configarationWithMinimumTime = {}

    # находим минимальное время обработки между наименьшими конфигурациями возможными
    configarationWithMinimumTime[min(suitableCPUForThisBudget.items(), key=lambda x: x[1][0])[0]] = [
        min(suitableCPUForThisBudget.items(), key=lambda x: x[1][0])[1]]
    MINiMIN = min(suitableCPUForThisBudget.items(), key=lambda x: x[1][0])[1][0]
    # сравним это минимальное время со временем в остальных конфигурациях с наибольшим значением

    for key, val in suitableCPUForThisBudget.items():
        if val[1] <= MINiMIN:
            configarationWithMinimumTime[key] = val

    print(configarationWithMinimumTime)

    return configarationWithMinimumTime


def findBestMachines(configarationWithMinimumTime, limitBudget, numberOfMachines, memoryOfTask, G, CPUOfTask):
    timeForTransferData = numberOfMachines * memoryOfTask / 50
    memoryBest = math.inf
    bestTime = math.inf
    for key, val in configarationWithMinimumTime.items():
        for j in range(len(memory)):
            for z in range(len(HDD)):
                setOfAllMachines = setOfMachines(numberOfMachines)
                for resource in range(numberOfMachines):
                    m1 = machine()
                    m1.CPU = CPU[key]
                    m1.memory = memory[j]
                    m1.HDD = HDD[z]
                    m1.availability = "free"
                    m1.price = price[key] + memory[j] / 3000 + HDD[z] / 30000
                    setOfAllMachines.addMachines(m1)

                timeForConf, budgetForConf = calculateTimeAndPrice(CPUOfTask, memoryOfTask, numberOfMachines,
                                                                   setOfAllMachines, G)
                # print(timeForMinConf, budgetForMinConf)

                # считаем время и стоимость для максимальной конфигурации текущего CPU

                if (timeForConf + timeForTransferData) <= bestTime and limitBudget >= budgetForConf:
                    bestTime = timeForConf
                    budget = budgetForConf
                    CPUBest = key
                    memoryBest = j
                    HDDBest = z

    print("CPUBest", CPU[key], "memoryBest", memory[memoryBest], "HDDBest", HDD[HDDBest], "bestTime", bestTime,
          "bestBudget in USD", budget)
    return CPUBest, memoryBest, HDDBest, bestTime, budget


# общий алгоритм
def bestConfuguration(limitBudget, numberOfMachines,CPUOfTask, memoryOfTask, G):
    suitableCPUForThisBudget = selectSeveralSuitableConfigaration(limitBudget, numberOfMachines,  CPUOfTask, memoryOfTask, G) # budgetLimit, numberOfMachines
    if len(suitableCPUForThisBudget) < 1:
        return -1
    else:
        configarationWithMinimumTime = findMinimumTimeFromSuitableMachines(suitableCPUForThisBudget)
        bestMachine = findBestMachines(configarationWithMinimumTime, limitBudget, numberOfMachines,memoryOfTask, G, CPUOfTask)
        return bestMachine

