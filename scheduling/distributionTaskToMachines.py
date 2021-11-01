from scheduling.taskForFurstNode import memoryOfTask, partOfTask, CPUOfTask, calculationOfExecutionTime, numberOfMachines
from scheduling.taskForFurstNode import calculateThePartsOfTask
from scheduling.setOfAvailableMachines import setOfMachines
from scheduling.setOfAvailableMachines import setOfAllMachines


def findMachineAndExecuteTask(indexOfTask, currentTime, dictTimeDone, setOfAllMachines):

    dictTimeDone[indexOfTask]["start"] = currentTime
    requiredMemory = memoryOfTask * partOfTask[indexOfTask]
    bestFreeMachine= setOfAllMachines.freeMachineWithBestCPUWithRequiredMemory(0, currentTime)
    #print(bestFreeMachine)
    while bestFreeMachine == None:
        bestFreeMachine = setOfAllMachines.freeMachineWithBestCPUWithRequiredMemory(0, currentTime)
        currentTime += 1
    #print("bestFreeMachine", bestFreeMachine)
    setOfAllMachines.assignMachineBusy(bestFreeMachine.name)
    executedTime = calculationOfExecutionTime(CPUOfTask * partOfTask[indexOfTask], bestFreeMachine.CPU, memoryOfTask * partOfTask[indexOfTask], bestFreeMachine.HDD)
    #print(executedTime, CPUOfTask * partOfTask[indexOfTask])
    currentTime += executedTime
    dictTimeDone[indexOfTask]["finish"] = currentTime
    dictTimeDone[indexOfTask]["nameOfMachine"] = bestFreeMachine.name
    dictTimeDone[indexOfTask]["done"] = "Yes"
    dictTimeDone[indexOfTask]["outMemory"] = requiredMemory + 5
    setOfAllMachines.assignMachineFree(bestFreeMachine.name, currentTime)

    return currentTime  # передается время освобождения



def distributionTaskToMachines(prioritet, commonTime, dictTimeDone,setOfAllMachines):
    from queue import PriorityQueue
    q = PriorityQueue()
    for task in prioritet:
        q.put((-dictTimeDone[task]["partOfTask"], task))
    #print(q)
    while not q.empty():
            while len(setOfAllMachines.setOfFreeMachines(commonTime)) < 1:
                    commonTime += 1
                    #print("commonTime+1", commonTime)
            #print(len(setOfAllMachines.setOfFreeMachines(commonTime)))
            for o in range(len(setOfAllMachines.setOfFreeMachines(commonTime))):
                if not q.empty():
                    next_item = q.get()
                    #print(next_item)
                    currentTime = commonTime
                    findMachineAndExecuteTask(next_item[1], currentTime, dictTimeDone, setOfAllMachines)
                    #print("1")

            #print("commonTime", commonTime)
    return commonTime


def distribitionTaskInMachines(numberOfMachines, CPUOfTask, memoryOfTask, G, allMachines):
    # for first node 1
    partOfTask = calculateThePartsOfTask(G)

    numberOfMachines = len(allMachines.setMachines)
    print(numberOfMachines)

    dictTimeDone = {}
    for i in G.nodes():
        dictTimeDone[i] = {"done": "No", "start": None, "finish": None, "nameOfMachine": None, "outMemory": None,
                           "partOfTask": partOfTask[i]}

    commonTime = 0
    dictTimeDone[1]["start"] = commonTime
    requiredMemory = memoryOfTask * partOfTask[1]
    bestFreeMachine = allMachines.freeMachineWithBestCPUWithRequiredMemory(0, commonTime)
    allMachines.assignMachineBusy(bestFreeMachine.name)
    executedTime = calculationOfExecutionTime(CPUOfTask * partOfTask[1], bestFreeMachine.CPU,
                                              memoryOfTask * partOfTask[1], bestFreeMachine.HDD)
    commonTime += executedTime
    dictTimeDone[1]["finish"] = commonTime
    dictTimeDone[1]["nameOfMachine"] = bestFreeMachine.name
    dictTimeDone[1]["done"] = "Yes"
    dictTimeDone[1]["outMemory"] = requiredMemory + 5
    allMachines.assignMachineFree(bestFreeMachine.name, commonTime)

    # select child of first node can be execited, because theurs parents tasks is completed

    for i in G.nodes():
        # print(i)
        firstPrioritet = set()
        secondPrioritet = set()
        for node in list(G.neighbors(i)):
            if dictTimeDone[node]["done"] != "Yes":
                execParentTask = list(
                    filter(lambda parent: dictTimeDone[parent]["done"] == "No", list(G.predecessors(node))))
                if len(execParentTask) > 0:
                    firstPrioritet.update(execParentTask)
                    secondPrioritet.add(node)
                else:
                    firstPrioritet.add(node)
                # print(firstPrioritet)

        if len(firstPrioritet) > 0:
            commonTime = distributionTaskToMachines(firstPrioritet, commonTime, dictTimeDone, allMachines)
        if len(secondPrioritet) > 0:
            commonTime = distributionTaskToMachines(secondPrioritet, commonTime, dictTimeDone, allMachines)

    return dictTimeDone