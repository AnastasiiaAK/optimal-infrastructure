
# набор машин из AWS Amazon
CPU = [8,16,64, 96]
memory = [16,32,64,128, 256]
HDD = [475,600,2400,3600]
price = [0.3616, 0.824, 3.616, 5.712]  # USD цены по каждому CPU.
# Почасовой тариф. Цена меняется только в зависомоти от CPU.
# по остальным параметрам взяты средние, потому что не значительно менются в цене.

# рассчитываем стоимость каждой конфигурации и стоимость сети в зависимости от количесвта машин и соединений
# ищем коэффициерт зависимости времени от cpu для каждой задачи (в данном упрощенном случае подчиняется закону гиперболы


class setOfMachines():
    setMachines = []

    def __init__(self, numbersOfMachines):
        self.numbersOfMachines = numbersOfMachines
        self.setFreeMachines = []
        self.setMachines = []

    def addMachines(self, machine):
        self.setMachines.append(machine)

    def setOfFreeMachines(self):
        self.setFreeMachines = []
        for i in self.setMachines:
            if i.availability == "free":
                self.setFreeMachines.append(i)
        return self.setFreeMachines

    def freeMachineWithBestCPUWithRequiredMemory(self, requiredMemory):
        bestCPU = 0
        machineWithBestCPU = 0
        for i in self.setMachines:
            if i.memory >= requiredMemory and i.CPU > bestCPU and i.availability == "free":
                machineWithBestCPU = i
                bestCPU = i.CPU
        if bestCPU == 0:
            return None
        else:
            return machineWithBestCPU

    def averageValuesOfFreeMachines(self):

        averageCPU = sum([i.CPU for i in self.setMachines]) / len(self.setMachines)
        averageMemory = sum([i.memory for i in self.setMachines]) / len(self.setMachines)
        averageHDD = sum([i.HDD for i in self.setMachines]) / len(self.setMachines)

        return averageCPU, averageMemory, averageHDD

    def priceOfAllAvailableMachines(self):
        commonPriceOfAllMachines = sum([i.price for i in self.setMachines])
        return commonPriceOfAllMachines


class machine():
    def CPU(self, CPU):
        self.CPU = CPU

    def memory(self, memory):
        self.memory = memory

    def HDD(self, HDD):
        self.HDD = HDD

    def availability(self, available):
        self.available = available

    def price(self, price):
        self.price = price

def plotDependenciesOfCPUForParticulatTask(cpuOfTask):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0.1, cpuOfTask * 100, 400)
    y = np.linspace(0.1, 50, 400)
    x, y = np.meshgrid(x, y)

    def axes():
        plt.axhline(0, alpha=.1)
        plt.axvline(0, alpha=.1)
        plt.xlabel("CPU of machine")
        plt.ylabel("Execution time")
        plt.title("Dependencies CPU of machine and execution time for Task with CPU = %s" % cpuOfTask)

    a = 2
    b = 1
    axes()
    plt.contour(x, y, (y - cpuOfTask * 10 / (x)), [0], colors='k')
    plt.show()


plotDependenciesOfCPUForParticulatTask(20)

def calculationOfExecutionTime(cpuOfTask, cpuOfMachine, MemoryOfTask, HDDOfMachine): # считаем время выполнения задачи на определнной машине
    executionTime = cpuOfTask*10/cpuOfMachine + MemoryOfTask/HDDOfMachine
    return executionTime

#print(calculationOfExecutionTime(76, 64, 13, 15), 'secоnds')
#print(calculationOfExecutionTime(76, 96, 13, 15), 'seconds')


def calculateThePartsOfTask(G):
    dTree = {}
    dTree[1] = 1
    for node in G.nodes():
        childNodes = list(G.neighbors(node))
        if len(childNodes) != 0:
            for child in childNodes:
                if child in dTree:
                    dTree[child] += dTree[node] / len(childNodes)
                else:
                    dTree[child] = dTree[node] / len(childNodes)
    return dTree
