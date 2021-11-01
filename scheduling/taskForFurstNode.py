from scheduling.setOfAvailableMachines import *
from scheduling.generateTask import G


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

def calculationOfExecutionTime(cpuOfTask, cpuOfMachine, MemoryOfTask, HDDOfMachine): # считаем время выполнения задачи на определнной машине
    executionTime = cpuOfTask*10/cpuOfMachine + MemoryOfTask/HDDOfMachine
    return executionTime

# for first node 1
partOfTask = calculateThePartsOfTask(G)


dictTimeDone = {}
for i in G.nodes():
    dictTimeDone[i] = {"done":"No","start":None, "finish":None, "nameOfMachine":None, "outMemory":None, "partOfTask" :partOfTask[i]}

commonTime = 0
dictTimeDone[1]["start"] = commonTime
requiredMemory = memoryOfTask * partOfTask[1]
bestFreeMachine= setOfAllMachines.freeMachineWithBestCPUWithRequiredMemory(0, commonTime)
setOfAllMachines.assignMachineBusy(bestFreeMachine.name)
executedTime = calculationOfExecutionTime(CPUOfTask * partOfTask[1], bestFreeMachine.CPU, memoryOfTask * partOfTask[1], bestFreeMachine.HDD)
commonTime += executedTime
dictTimeDone[1]["finish"] = commonTime
dictTimeDone[1]["nameOfMachine"] = bestFreeMachine.name
dictTimeDone[1]["done"] = "Yes"
dictTimeDone[1]["outMemory"] = requiredMemory + 5
setOfAllMachines.assignMachineFree(bestFreeMachine.name, commonTime)
