"""
Experiment is a script that runs multiple iterations of GFS, calculates means and
plots average results over generations and at shows the best permutation that has been found
"""

import json
import statistics
import time

import numpy as np
from gfs import GeneticFlowShop
from util import get_machine_names, get_task_names, read_operations, average_of_list, who_is_the_best
import matplotlib.pyplot as plt
import os
from gantt_fs import create_and_show_gantt_fs


def main():
    
    n_iter = 10
    
    # Number of population
    n_pop = 3
    # Probability of crossover
    p_cross = 1.00
    # Probability of mutation
    p_mut = 1.00
    # Stopping number for generation
    n_epoch = 1000


    n, m = 500, 20
    operation_times = read_operations(n, m)



    n_pop_values = list(range(3,10+1))
    p_cross_values = list(np.linspace(start=0.0, stop=1.0, num=5, endpoint=True))
    p_mut_values = list(np.linspace(start=0.0, stop=1.0, num=5, endpoint=True))

    
    for p_cross in p_cross_values:
        for p_mut in p_mut_values:
            for n_pop in n_pop_values:
                print(f"=========== {p_cross=} {p_mut=} {n_pop=} =========")

                # Initialize specific makespans for each epoch of every iteration
                best_makespans = []
                worst_makespans = []
                average_makespans = []
                best_permutations_of_the_experiment_with_makespans = []


                for i in range(n_iter):
                    print(f"Iteration: {i+1}/{n_iter}")
                    
                    # Run single iteration
                    gfs = GeneticFlowShop(  m, n, operation_times, 
                                            n_pop, p_cross, p_mut, n_epoch)
                    t1 = time.process_time() # Start Timer
                    gfs.run()
                    t2 = time.process_time() # Stop Timer
                    # gfs.plot()
                    # plt.show(block=True)

                    

                    # Collect result
                    best_makespans.append(gfs.best_specimen)
                    # worst_makespans.append(gfs.worst_specimen)
                    average_makespans.append(gfs.average_specimen)
                    best_permutations_of_the_experiment_with_makespans.append(gfs.best_permutation_with_makespan)





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
                    with open("results\myfile.txt", "a") as file1:
                        file1.write(f"N_iter: {n_iter} N_pop: {n_pop} P_c: {p_cross} P_m: {p_mut} Best_makespan: {bestest_makespan} Average_makespan: {averagest_of_best_makespans} St_dev: {st_dev}\n")
                    
                    
                    
                    
                    single_best_permutation, single_best_makespan = who_is_the_best(best_permutations_of_the_experiment_with_makespans)

                    fig, ax = plt.subplots()
                    ax.set(xlabel='Generation', ylabel='Makespan',
                        title=f'Average values of makespans for {n_iter} iterations of Genetic Flow Shop algorithm')
                    
                    ax.plot(range(0, n_epoch), best_makespans[i], label="best makespan")
                    # ax.plot(range(0, n_epoch), worst_makespans[i], label="worst makespan")
                    ax.plot(range(0, n_epoch), average_makespans[i], label="average makespan")
                    plt.legend()
                    ax.grid()


                    plt.draw()
                    # plt.pause(0.5)
                    # plt.show()

                    if not os.path.exists("./results/"):
                        os.mkdir("./results/")
                        
                    fig.savefig("./results/test.png")


                    # show gantt diagram
                    # best_schedule = gfs.get_schedule(single_best_permutation)
                    best_schedule = gfs.get_schedule()
                    machine_names = get_machine_names(m)
                    job_names = get_task_names(n)
                    # create_and_show_gantt_fs(best_schedule, machine_names, job_names)

                    # # Write results to file
                    # d={"Iter": i, "N_pop": n_pop, "P_c": p_cross, "P_m": p_mut}
                    # json_string = json.dumps(d)
                    # with open('json_data.json', 'a') as outfile:
                    #     json.dump(json_string, outfile)
                else:
                    raise Exception("Sorry, length of best, worst and avergae makespans list do not match n_epoch")



if __name__ == '__main__':
    main()