from newSelectMachinesWithHrZ.find_optimal_minimum_and_maximum_numbers_of_machine import *

maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration = max_number_of_machine(9000,
                                                                                   sorted_list_of_configuration_machine,0)
maximum_available_number_of_machines_with_this_price_limit_expensive_configuration = max_number_of_machine(9000,
                                                                                   sorted_list_of_configuration_machine,15)
print("maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration",
      maximum_available_number_of_machines_with_this_price_limit_cheapest_configuration,
      "maximum_available_number_of_machines_with_this_price_limit_expensive_configuration",
      maximum_available_number_of_machines_with_this_price_limit_expensive_configuration, sep="\n")


# take