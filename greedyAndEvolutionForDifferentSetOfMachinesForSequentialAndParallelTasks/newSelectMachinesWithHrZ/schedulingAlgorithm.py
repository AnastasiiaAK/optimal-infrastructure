from newSelectMachinesWithHrZ.algorithmOfParalleltask import *

number_of_machine = 3
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(1)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)


common_time, schedule_in_dataframe = distribution_tasks_to_machines(taskGraph, descriptionOffTask, machines)
print(common_time)
print(schedule_in_dataframe)
