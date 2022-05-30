import time
from genetic import GeneticFlowShop
from util import read_operations

def main():
    # Number of population
    n_pop = 4
    # Probability of crossover
    p_cross = 1.0
    # Probability of mutation
    p_mut = 1.0
    # Stopping number for generation
    n_epoch = 100


    m, n = 5, 20
    operation_times = read_operations(m, n)


    # specific makespans for each epoch of every iteration
    best_makespans = []
    worst_makespans = []
    average_makespans = []
    for i in range(3):
        
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
        worst_makespans.append(gfs.worst_specimen)
        average_makespans.append(gfs.average_specimen)

    x = 5

    # average of specific makespans for each epoch of every iteration
    best_makespans = []
    worst_makespans = []
    average_makespans = []    

if __name__ == '__main__':
    main()