# будем роаспределять задания по машинам
numberOfMachines = 4
CPUOfTask = 100
memoryOfTask = 20

CPU = [8, 16, 64, 96]
memory = [16, 32, 64, 128, 256]
HDD = [475, 600, 2400, 3600]

price = [0.3616, 0.824, 3.616, 5.712]


class setOfMachines():
    setMachines = []

    def __init__(self, numbersOfMachines):
        self.numbersOfMachines = numbersOfMachines
        self.setFreeMachines = []
        self.setMachines = []

    def addMachines(self, machine):
        self.setMachines.append(machine)

    def setOfFreeMachines(self, currentTime):
        self.setFreeMachines = []
        for i in self.setMachines:
            if i.availability == "free" and i.timeOfDeliverance < currentTime:
                self.setFreeMachines.append(i)
        return self.setFreeMachines

    def freeMachineWithBestCPUWithRequiredMemory(self, requiredMemory, currentTime):
        bestCPU = 0
        for i in self.setMachines:
            if i.availability == "free" and i.timeOfDeliverance < currentTime and i.CPU > bestCPU:
                machineWithBestCPU = i
                bestCPU = i.CPU
        return machineWithBestCPU

    def averageValuesOfFreeMachines(self):

        averageCPU = sum([i.CPU for i in self.setMachines]) / len(self.setMachines)
        averageMemory = sum([i.memory for i in self.setMachines]) / len(self.setMachines)
        averageHDD = sum([i.HDD for i in self.setMachines]) / len(self.setMachines)

        return averageCPU, averageMemory, averageHDD

    def priceOfAllAvailableMachines(self):
        commonPriceOfAllMachines = sum([i.price for i in self.setMachines])
        return commonPriceOfAllMachines

    def assignMachineBusy(self, numberOfMachine):
        self.setMachines[numberOfMachine].availability = "busy"

    def assignMachineFree(self, numberOfMachine, timeOfDeliv):
        self.setMachines[numberOfMachine].availability = "free"
        self.setMachines[numberOfMachine].timeOfDeliverance = timeOfDeliv


class machine():
    def name(self, name):
        self.name = name

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

    def timeOfDeliverance(self, timeOfDeliverance):
        self.timeOfDeliverance = timeOfDeliverance


import random

numberOfMachines = 4
setOfAllMachines = setOfMachines(4)

# generate parameters of machines
for i in range(numberOfMachines):
    a = random.random()
    b = random.random()
    c = random.random()

    m1 = machine()
    m1.name = i
    m1.CPU = CPU[round(a * (len(CPU) - 1))]
    m1.memory = memory[round(b * (len(memory) - 1))]
    m1.HDD = HDD[round(c * (len(HDD) - 1))]
    m1.availability = "free"
    m1.price = price[round(a * (len(price) - 1))]
    m1.timeOfDeliverance = -2
    setOfAllMachines.addMachines(m1)

# берем первое задание и кладем его в на самы йлучший компьютер, потому что без выполненного первого задания другие не могут выполняться, поэтому нужна максчимальная скорость выполненения