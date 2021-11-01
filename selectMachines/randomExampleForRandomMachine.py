from generateTask import G
from setParametersOfMachine import *
from calculateTimeInEachMachine import calculateTimeAndPrice


import random


CPUOfTask = 10
memoryOfTask = 15

numberOfMachines = 5
setOfAllMachines = setOfMachines(5)

# generate parameters of machines
for i in range(numberOfMachines):
    a = random.random()
    b = random.random()
    c = random.random()

    m1 = machine()
    m1.CPU = CPU[round(a * (len(CPU) - 1))]
    m1.memory = memory[round(b * (len(memory) - 1))]
    m1.HDD = HDD[round(c * (len(HDD) - 1))]
    m1.availability = "free"
    m1.price = price[round(a * (len(price) - 1))]
    m1.timeOfDeliverance = -1
    setOfAllMachines.addMachines(m1)

calculateTimeAndPrice(100, 20, 3, setOfAllMachines, G)
