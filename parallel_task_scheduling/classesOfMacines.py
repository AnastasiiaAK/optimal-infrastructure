from parameters import *


class ConfigurationOfMachines:
    def __init__(self, id_of_machine, id_of_configuration, cpu, is_available='free', time_of_deliverance=-1):
        self.available = is_available
        self.CPU = cpu
        self.core_freq = dictFreq[id_of_configuration]
        self.price = dictWithPrices[id_of_configuration][cpu]
        self.id_of_configuration = id_of_configuration
        self.id = id_of_machine
        self.time_of_deliverance = time_of_deliverance

    def total_cost(self, time_of_work):
        return time_of_work * 60 * self.price

    def availability(self, current_time):
        if current_time >= self.time_of_deliverance:
            self.available = "free"
        else:
            self.available = "busy"
        return self.available

    def working_time_with_particular_task(self, task, task_cpu):
        execution_time = task_cpu * 3.7 / self.core_freq / ((self.CPU - 1) * float(task["possibilityOfParalleling"]) + 1)
        # 3.7 - meaning of core_freq of my computer.
        return execution_time

    def make_machine_busy(self, finish_time):
        self.available = "busy"
        self.time_of_deliverance = finish_time

    def make_machine_free(self, ):
        self.available = "free"


class ConfigurationOfSwitches:
    def __init__(self, common_number_of_machines):
        if common_number_of_machines <= 4:
            id_of_swithes = 1
        elif common_number_of_machines > 8:
            id_of_swithes = 3
        else:
            id_of_swithes = 2

        self.id_of_switches = id_of_swithes
        self.frequency = dictSwitches[self.id_of_switches]["frequency"]
        self.price = dictSwitches[self.id_of_switches]["price"]
        self.attached_devices = dictSwitches[self.id_of_switches]["number_attached"]

    '''
    transfer time calculated as:
    780 - is HDD of reference example
    8 seconds (time for distribution to 1 machine) - is received from  solving system of linear equation (data get from testing task with 1, 2, 3 machine)
    suggestion - that the frequency os switch (on the machine on which it was tested)
    So, result formula is frequency / 780 * current_HDD * number_of_machine
    '''

    def calculate_transfer_time_to(self, number_of_using_machines, task):
        memory_of_task = float(task["incomingMemory"])
        transfer_time = (memory_of_task / (self.frequency / number_of_using_machines))
        transfer_time = (self.frequency / 780 * memory_of_task) * number_of_using_machines
        # transfer_rate = self.frequency * 71 / number_of_using_machines
        # transfer_time = memory_of_task / transfer_rate
        return transfer_time

    def calculate_transfer_time_from(self, number_of_using_machines, task):
        memory_of_task = float(task["outgoingMemory"])
        transfer_time = (memory_of_task / (self.frequency / number_of_using_machines))
        transfer_time = (self.frequency / 780 * memory_of_task) * number_of_using_machines
        # transfer_rate = self.frequency * 71 / number_of_using_machines
        # transfer_time = memory_of_task / transfer_rate
        return transfer_time

    def calculate_transfer_time(self, number_of_using_machines, task):
        memory_of_task = float(task["incomingMemory"])
        transfer_time = (memory_of_task / (self.frequency / number_of_using_machines))
        transfer_time = (self.frequency / 780 * memory_of_task) * number_of_using_machines

        # transfer_rate = self.frequency * 71 / number_of_using_machines
        # transfer_time = memory_of_task / transfer_rate
        return transfer_time

    def calculate_transfer_price(self, number_of_using_machines, task):
        memory_of_task = float(task["incomingMemory"])
        transfer_time = (memory_of_task / (self.frequency / number_of_using_machines))
        transfer_time = (self.frequency / 780 * memory_of_task) * number_of_using_machines
        # transfer_rate = self.frequency * 71
        # transfer_time = memory_of_task / transfer_rate * number_of_using_machines
        return transfer_time * self.price


class SetOfMachines:
    def __init__(self, number_of_machines):
        self.number_of_machines = number_of_machines
        self.listOfMachines = []
        self.listOfFreeMachines = []

    def add_machine(self, machine):
        self.listOfMachines.append(machine)

    def add_switch(self, switch):
        self.switch = switch

    def list_of_free_machines(self, current_time):
        self.listOfFreeMachines = []
        for machine in self.listOfMachines:
            if machine.availability(current_time) == 'free':
                self.listOfFreeMachines.append(machine)
        return self.listOfFreeMachines

    def find_best_free_machines(self, task, current_time):
        self.listOfFreeMachines = []
        for machine in self.listOfMachines:
            if machine.availability(current_time) == 'free':
                self.listOfFreeMachines.append(machine)

        best_machine = self.listOfFreeMachines[0]
        best_conf = 0
        if float(task["possibilityOfParalleling"]) > 0.3:
            for machines in self.listOfFreeMachines:
                current_conf = machines.CPU * machines.core_freq
                if current_conf > best_conf:
                    best_conf = current_conf
                    best_machine = machines
        else:
            min_number_of_cpu = min(CPU)
            for machines in self.listOfFreeMachines:
                if machines.CPU == min_number_of_cpu:
                    current_conf = machines.core_freq
                    if current_conf > best_conf:
                        best_conf = current_conf
                        best_machine = machines

        return best_machine








