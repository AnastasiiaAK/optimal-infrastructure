
from selectMachines.setParametersOfMachine import calculateThePartsOfTask, calculationOfExecutionTime

def calculateExecutedTimeInEachNode(parentNode, CPUOfTask, memoryOfTask,setOfAllMachines, G, visited=[]):
    partsOfTask = calculateThePartsOfTask(G)
    childNodes = G.neighbors(parentNode)
    # print(list(G.adjacency()))
    # print(list(G.neighbors(parentNode)))

    numbersOfChildNodes = len(list(G.neighbors(parentNode)))

    # print(list(childNodes), numbersOfChildNodes, len(list(childNodes)))

    # CPUOfTask = CPUOfTask + 10
    # memoryOfTask = memoryOfTask + 10
    calculationOfExecutionTimes = 0
    # print(parentNode, numbersOfChildNodes)
    # if numbersOfChildNodes != 0:

    #    onePartOfTask = partsOfTask[list(childNodes)[0] - 1]

    if numbersOfChildNodes == 1 and list(G.neighbors(parentNode))[0] not in visited:

        onePartOfTask = partsOfTask[list(G.neighbors(parentNode))[0]]

        # считаем время выполнения задачи на какой-то машине с учетом CPU и HDD

        # здесь считаем как будто задача выполлняется на одной машине
        # calculationOfExecutionTimeCPU = calculationOfExecutionTime(CPUOfTask, setOfAllMachines.freeMachineWithBestCPUWithRequiredMemory(memoryOfTask).CPU, memoryOfTask, setOfAllMachines.freeMachineWithBestCPUWithRequiredMemory(memoryOfTask).HDD)

        # здесь считаем, что выполняется параллельно на всех свободных машинах. Считаем время для средних значений на всех машинах и делим на общее кол-во свободных машин

        numberOfFreeMachines = len(setOfAllMachines.setOfFreeMachines())

        calculationOfExecutionTimeParalell = calculationOfExecutionTime(CPUOfTask * onePartOfTask,
                                                                        setOfAllMachines.averageValuesOfFreeMachines()[
                                                                            0], memoryOfTask * onePartOfTask,
                                                                        setOfAllMachines.averageValuesOfFreeMachines()[
                                                                            2]) / numberOfFreeMachines
        # print(onePartOfTask,calculationOfExecutionTimeParalell)
        calculationOfExecutionTimes += calculationOfExecutionTimeParalell

        CPUOfTask = CPUOfTask + 10
        memoryOfTask = memoryOfTask + 10

        # предположим, что параметры задания увеличиваются с каждой дальнейшей операцией


    elif numbersOfChildNodes > 1:

        calculationOfExecutionTimes = 0
        for i in G.neighbors(parentNode):
            if i not in visited:
                onePartOfTask = partsOfTask[i]
                numberOfFreeMachines = len(setOfAllMachines.setOfFreeMachines())
                calculationOfExecutionTimes += calculationOfExecutionTime(CPUOfTask * onePartOfTask,
                                                                          setOfAllMachines.averageValuesOfFreeMachines()[
                                                                              0], memoryOfTask * onePartOfTask,
                                                                          setOfAllMachines.averageValuesOfFreeMachines()[
                                                                              2]) / len(
                    setOfAllMachines.setOfFreeMachines())

        CPUOfTask = (CPUOfTask + 10)
        memoryOfTask = (memoryOfTask + 10)

    elif numbersOfChildNodes == 0:
        calculationOfExecutionTimes = 0
        CPUOfTask = 0
        memoryOfTask = 0

    visited.extend(list(childNodes))

    return calculationOfExecutionTimes, CPUOfTask, memoryOfTask, visited

# нужно как-то добавить время передачи данных по проводам. Скорее всего это зависит от количесвта машин на которые мы распределяемю.
# пусть оно зависит от параметра memory.

def calculateTimeAndPrice(CPUOfTask, memoryOfTask, numberOfMachines, setOfAllMachines, G):
    # put the parameters of tasks
    currentTime = 0
    outCPUOfTask = CPUOfTask
    outMemoryOfTask = memoryOfTask

    commonPrice = 0  # стоимость работы. зависит от времени и машин

    numberOfFreeMachines = len(setOfAllMachines.setOfFreeMachines())
    calculationOfExecutionTimeParalell = calculationOfExecutionTime(CPUOfTask,
                                                                    setOfAllMachines.averageValuesOfFreeMachines()[0],
                                                                    memoryOfTask,
                                                                    setOfAllMachines.averageValuesOfFreeMachines()[
                                                                        2]) / numberOfFreeMachines
    currentTime = calculationOfExecutionTimeParalell  # ставим время выполнения певрого задания за первоначальное
    # commonPrice = sum(price) * currentTime

    visited = []
    for parentNode in G.nodes():
        calculationOfExecutionTimeInChildNodes, outCPUOfTask, outMemoryOfTask, visited = calculateExecutedTimeInEachNode(
            parentNode, outCPUOfTask, outMemoryOfTask,setOfAllMachines, G, visited)
        currentTime += calculationOfExecutionTimeInChildNodes
        # print(calculationOfExecutionTimeInChildNodes)
        # commonPrice += sum(price) * currentTime

        # print(parentNode, calculationOfExecutionTimeInChildNodes)

    # print("Time of all calculation is ",currentTime)
    # print("Common price for one workflow in USD (depends on time)", currentTime * setOfAllMachines.priceOfAllAvailableMachines())

    # пусть количевсто компьютеров и memory имеют прямую зависимость со временем выполнения

    timeForTransferData = numberOfMachines * memoryOfTask / 50

    commonTime = currentTime + timeForTransferData

    # print("Common time for calculation and transfer",commonTime )
    return commonTime, currentTime * setOfAllMachines.priceOfAllAvailableMachines()