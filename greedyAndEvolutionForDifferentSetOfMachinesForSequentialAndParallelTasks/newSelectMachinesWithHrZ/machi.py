from classesOfMacines import *
number_of_machine = 3
machines = SetOfMachines(number_of_machine)
switch = ConfigurationOfSwitches(1)
for i in range(1, number_of_machine + 1):
    machine = ConfigurationOfMachines(i, 1, 4, 'free')
    machines.add_machine(machine)
machines.add_switch(switch)


current_time = 3

m = machines.listOfMachines[0]
m.make_machine_busy(6)

#print(len(machines.list_of_free_machines(current_time)))
#print(machines.list_of_free_machines(current_time))
print(machines.list_of_free_machines(10))
print(machines.list_of_free_machines(current_time))


