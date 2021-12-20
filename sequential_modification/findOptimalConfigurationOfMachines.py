# from sequential_modification.classesOfMacines import *
from sequential_modification.algorithmOfParalleltask import *


'''
number_of_machine = 16

# set number of task

machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 4, 16, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)

common_time, schedule_in_dataframe = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
print(common_time)
# find minimum of executing task

number_of_machine = 1

# set number of task
number_of_task = 7


machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 2, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)

common_time, schedule_in_dataframe = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
print(common_time)


# lets find with cheapest configuration
number_of_machine = 1
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 2, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)
# common_time = 1087.8438

# lets find with the most expensive configuration
number_of_machine = 16
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(number_of_machine)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 4, 16, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)
# common_time = 12.735842285714288
'''



import numpy as np
x = np.linspace(1, 16, 16, dtype=int)
list_of_y = []
list_of_x = []
for mac in x:

    number_of_task = 7
    # set graph of task (sequential)
    taskGraph = set_task(number_of_task)

    data = [[0, 0, round(0.11952686309814453, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [1, 1, round(0.38246989250183105, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [2, 2, round(0.0005393028259277344, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [3, 3, round(1.6666145324707031, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [4, 4, round(1451.2022745609283, 2), 0, 0, 1, None, None, None, None, None, "No"],
            [5, 5, round(0.67854, 2), 0, 0, 0, None, None, None, None, None, "No"],
            [6, 6, round(0.4834657, 2), 0, 0, 0, None, None, None, None, None, "No"]]

    descriptionOffTask = pd.DataFrame(data, columns=['indexOfTask', "nameOfTask", "complexityOfTask", "incomingMemory",
                                                     "outgoingMemory", "possibilityOfParalleling", "idOfMachine",
                                                     "startTime", "endTime", "executingTime", "transferPrice", "done"])

    def find_common_price(data_table):
        overall_price = 0
        if type(data_table["idOfMachine"]) == list:
            for m in data_table["idOfMachine"]:
                overall_price += pricesOfUsingMachines[m] * data_table["executingTime"]
            return overall_price
        return pricesOfUsingMachines[data_table["idOfMachine"]] * data_table["executingTime"]


    number_of_machine = mac
    pricesOfUsingMachines = {}
    machines = SetOfMachines(mac)
    switch = ConfigurationOfSwitches(mac)
    for i in range(1, number_of_machine + 1):
        machine = ConfigurationOfMachines(i, 1, 4, 'free')
        machines.add_machine(machine)
        pricesOfUsingMachines[machine.id] = machine.price
    machines.add_switch(switch)
    common_time, scheduling_table = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)

    price_of_all_working = sum(scheduling_table.apply(find_common_price, axis=1))
    list_of_y.append(price_of_all_working + sum(scheduling_table["transferPrice"]))
    list_of_x.append(common_time)


plt.plot(list_of_x, list_of_y)
plt.title("Dependence of the working time on the number of machines ")
plt.ylabel("Price")
plt.xlabel("Working time")
plt.show()

