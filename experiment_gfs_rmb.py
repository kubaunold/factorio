"""
Experiment is a script that runs multiple iterations of GFS with RMB, calculates means and
plots average results over generations and at shows the best permutation that has been found
"""

import time
from unittest.mock import NonCallableMock
from gfs_rmb import GeneticFlowShopWithMachineBreakdown
from util import get_machine_names, get_task_names, read_operations, average_of_list, who_is_the_best
import matplotlib.pyplot as plt
import os
from gantt_fs import create_and_show_gantt_fs


def main():
    
    n_iter = 5
    
    # Number of population
    n_pop = 4
    # Probability of crossover
    p_cross = .05
    # Probability of mutation
    p_mut = .07
    # Stopping number for generation
    n_epoch = 1000


    m, n = 10, 50
    operation_times = read_operations(m, n)
    # Failure size
    failure_size = 0.03

    # specific makespans for each epoch of every iteration
    best_makespans = []
    worst_makespans = []
    average_makespans = []
    best_permutations_of_the_experiment_with_makespans = []
    breakdown = None

    for i in range(n_iter):
        
        # Run single iteration
        gfsrmb = GeneticFlowShopWithMachineBreakdown(
            m, n, operation_times, 
            n_pop, p_cross, p_mut, n_epoch, 
            failure_size)
        t1 = time.process_time() # Start Timer
        gfsrmb.run()
        t2 = time.process_time() # Stop Timer
        # gfs.plot()
        # plt.show(block=True)

        breakdown = gfsrmb.breakdown

        # Collect result
        best_makespans.append(gfsrmb.best_specimen)
        worst_makespans.append(gfsrmb.worst_specimen)
        average_makespans.append(gfsrmb.average_specimen)
        best_permutations_of_the_experiment_with_makespans.append(gfsrmb.best_permutation_with_makespan)

    # average of specific makespans for each epoch of every iteration
    if len(best_makespans) == len(worst_makespans) == len(average_makespans) == n_iter:
        avg_of_best_makespans = average_of_list(best_makespans)
        avg_of_worst_makespans = average_of_list(worst_makespans)
        avg_of_average_makespans = average_of_list(average_makespans)
        
        single_best_permutation, single_best_makespan = who_is_the_best(best_permutations_of_the_experiment_with_makespans)

        fig, ax = plt.subplots()
        ax.set(xlabel='Generation', ylabel='Makespan',
            title=f'Average values of makespans for {n_iter} iterations of Genetic Flow Shop algorithm')
        
        ax.plot(range(0, n_epoch), best_makespans[i], label="best makespan")
        ax.plot(range(0, n_epoch), worst_makespans[i], label="worst makespan")
        ax.plot(range(0, n_epoch), average_makespans[i], label="average makespan")
        plt.legend()
        ax.grid()


        plt.draw()
        plt.pause(0.5)
        plt.show()

        if not os.path.exists("./results/"):
            os.mkdir("./results/")
            
        fig.savefig("./results/test.png")


        # show gantt diagram
        # best_schedule = gfsrmb.get_schedule(single_best_permutation)
        best_schedule = gfsrmb.get_schedule()
        machine_names = get_machine_names(m)
        job_names = get_task_names(n)
        create_and_show_gantt_fs(best_schedule, machine_names, job_names, breakdown)

    else:
        raise Exception("Sorry, length of best, worst and avergae makespans list do not match n_epoch")



if __name__ == '__main__':
    main()