"""
Experiment is a script that runs multiple iterations of GFS with RMB, calculates means and
plots average results over generations and at shows the best permutation that has been found
"""

import statistics
import time
from unittest.mock import NonCallableMock

import matplotlib
from gfs_rmb import GeneticFlowShopWithMachineBreakdown
from util import get_machine_names, get_task_names, read_operations, average_of_list, who_is_the_best
import matplotlib.pyplot as plt
import os
from gantt_fs import create_and_show_gantt_fs


matplotlib.interactive(True) # akk figures will be displayed instantaneously


def main():
    
    n_iter = 10
    
    # Number of population
    n_pop = 6
    # Probability of crossover
    p_cross = 1.0
    # Probability of mutation
    p_mut = 1.0
    # Stopping number for generation
    n_epoch = 1000


    n, m = 500, 20
    operation_times = read_operations(n, m)
    # Failure size
    failure_size = 0.10

    # specific makespans for each epoch of every iteration
    best_makespans = []
    # worst_makespans = []
    average_makespans = []
    best_permutations_of_the_experiment_with_makespans = []
    breakdown = None

    for i in range(n_iter):
        print(f"=========== {p_cross=} {p_mut=} {n_pop=} n_iter={i} =========")
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
        # worst_makespans.append(gfsrmb.worst_specimen)
        average_makespans.append(gfsrmb.average_specimen)
        best_permutations_of_the_experiment_with_makespans.append(gfsrmb.best_permutation_with_makespan)

    # average of specific makespans for each epoch of every iteration
    # if len(best_makespans) == len(worst_makespans) == len(average_makespans) == n_iter:
    if len(best_makespans) == len(average_makespans) == n_iter:
        avg_of_best_makespans = average_of_list(best_makespans)
        # avg_of_worst_makespans = average_of_list(worst_makespans)
        avg_of_average_makespans = average_of_list(average_makespans)
        
        bestest_makespans = [i[-1] for i in best_makespans]
        bestest_makespan = min(bestest_makespans)
        averagest_of_best_makespans = sum(bestest_makespans) / len(bestest_makespans)
        st_dev = statistics.stdev(bestest_makespans)

        # Write results to file
        with open(f"results\\fsrmb_n{n}_m{m}_pcross{p_cross}_pmut{p_mut}_npop{n_pop}.txt", "a") as f:
            f.write(f"P_c: {p_cross}\tP_m: {p_mut}\tN_pop: {n_pop}\tBest_makespan: {bestest_makespan} Average_makespan: {averagest_of_best_makespans} St_dev: {st_dev}\n")
            # f.write(f"P_c: {p_cross} P_m: {p_mut} N_pop: {n_pop}")
                    




        
        single_best_permutation, single_best_makespan = who_is_the_best(best_permutations_of_the_experiment_with_makespans)

        fig, ax = plt.subplots()
        fig.set_size_inches(18, 10)
        ax.set_title(
            f'Średnie wartości makespanu na przestrzeni wszystkich generacji AG rozwiązującego FSRMB dla {n_iter} iteracji',
            fontsize = 18,
        )
        ax.set_xlabel(
            'Generacja',
            fontsize = 16,
        )
        ax.set_ylabel(
            'Makespan',
            fontsize = 16,
        )
        
        ax.plot(range(0, n_epoch), best_makespans[i], label="średnia z najlepszych makespanów")
        # ax.plot(range(0, n_epoch), worst_makespans[i], label="worst makespan")
        ax.plot(range(0, n_epoch), average_makespans[i], label="średnia ze średnich makespanów")
        
        # Show textbox with parameter values
        textstr = '\n'.join((
            r'$P_{cross}=%.2f$' % (p_cross, ),
            r'$P_{mut}=%.2f$' % (p_mut, ),
            r'$N_{pop}=%d$' % (n_pop, ),))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
        # Show legend
        plt.legend(prop={'size': 14})
        
        ax.grid()


        plt.draw()
        plt.pause(0.5)
        plt.show()

        if not os.path.exists("./results/"):
            os.mkdir("./results/")
            
        fig.savefig("./results/test.png")


        # show gantt diagram
        # best_schedule = gfsrmb.get_schedule(single_best_permutation)
        gfsrmb = GeneticFlowShopWithMachineBreakdown(
                    m, n, operation_times, 
                    n_pop, p_cross, p_mut, n_epoch, 
                    failure_size)
        gfsrmb.calculate_makespan(single_best_permutation)
        best_schedule = gfsrmb.get_schedule()
        machine_names = get_machine_names(m)
        job_names = get_task_names(n)
        create_and_show_gantt_fs(best_schedule, machine_names, job_names, breakdown, suspend_operation_names=(n>25))
        input("Press Enter to finish close program...")
    else:
        raise Exception("Sorry, length of best, worst and avergae makespans list do not match n_epoch")



if __name__ == '__main__':
    main()