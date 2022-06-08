""" class solving Flow Shop with Machine Breakdown using Genetic Algorithm """

from matplotlib import pyplot as plt
from gantt_fs import create_and_show_gantt_fs
from gfs import GeneticFlowShop
from base_logger import logger as logging
from util import read_operations, sum_of_list, get_machine_names, get_task_names
from random import randint
from breakdown import Breakdown

class GeneticFlowShopWithMachineBreakdown(GeneticFlowShop):
    def __init__(self, m, n, operation_times, n_pop, p_cross, p_mut, n_epoch, failure_size, plot_progress=True) -> list:
        super().__init__(m, n, operation_times, n_pop, p_cross, p_mut, n_epoch, plot_progress=True)
        self.failure_size = failure_size

        self.breakdown = self.__generate_breakdown()


    def __generate_breakdown(self):
        makespan = sum_of_list(self.op_times[0])
        breakdown_duration = max(randint(5,15), int(makespan * self.failure_size))

        return Breakdown(randint(0,self.m - 1), randint(0, makespan), breakdown_duration)

    def plot_sample(self):
        _ = self.calculate_makespan([0,2,1,3])
        some_schedule = self.get_schedule()

        machine_names = get_machine_names(self.m)
        job_names = get_task_names(self.n)
        create_and_show_gantt_fs(some_schedule, machine_names, job_names, breakdown=self.breakdown)




def main():
    logging.info("I'm inside GFS with RMB!.")

    # Number of population
    n_pop = 4
    # Probability of crossover
    p_cross = 1.0
    # Probability of mutation
    p_mut = 1.0
    # Stopping number for generation
    n_epoch = 100
    # Number of machines and tasks
    n, m = 4, 3

    # Read operation times
    operation_times = read_operations(m, n)

    # [0,1] - size of machine unavailability counted as failure_size * makespan
    failure_size = 0.05

    # Run single iteration
    gfsrmb = GeneticFlowShopWithMachineBreakdown(  m, n, operation_times, 
                            n_pop, p_cross, p_mut, n_epoch, failure_size)



    gfsrmb.plot_sample()
    
    x=5

if __name__ == '__main__':
    main()