"""
Module containing Genetic Flow Shop class definition. It expands FlowShop class by 
solving FS problem using Genetic Algorithm.

"""
import random
import time
from numpy import Inf
from numpy.random import permutation, choice
from fs import FlowShop
from util import read_operations, silnia
import mutation, crossover
from base_logger import logger as logging
import matplotlib.pyplot as plt
import os

class GeneticFlowShop(FlowShop):
    def __init__(   self, m, n, operation_times,
                    n_pop, p_cross, p_mut, n_epoch) -> list:
        super().__init__(m, n, operation_times)
        self.n_pop = n_pop
        self.p_cross = p_cross
        self.p_mut = p_mut
        self.n_epoch = n_epoch
        
        self.population = self.__get_initial_population()
        # list of best specimen for each epoch
        self.best_specimen = []
        self.worst_specimen = []
        self.average_specimen = []

        # List of tuples: best permutations across all generations with their makespans
        self.best_permutation_with_makespan = []

        # should I add here the following lines?
        # self.parents = []
        # self.children = []

    def __get_initial_population(self) -> list:
        """Creating the initial population (n_pop distinct chromosomes)"""

        pop = []
        allow_duplicate = False

        if self.n_pop > silnia(self.m):
            logging.warning("Warning! Size of the population exceeds number of possible permutations.py. There will be duplicate permutations.")
            allow_duplicate = True

        # Select specimen one by one
        for i in range(self.n_pop):
            p = list(permutation(self.n))
            if allow_duplicate:
                p = list(permutation(self.n))
            else:
                while p in pop:
                    p = list(permutation(self.n))

            pop.append(p)

        return pop

    def __selection(self) -> None:
        """ Select parents based on given population.
            Creates self.parents list. """
        
        # Create and purge parents for future incoming offspring
        self.parents = []

        # create list of tuples such as: (makespan, index)
        pop_w_makespan = []
        for i in range(self.n_pop):
            pop_w_makespan.append([self.calculate_makespan(self.population[i]), i]) 


        # sort by ascending value makespan (the fittest is at the beginning)
        pop_w_makespan.sort()


        # here update the best permutation in this generation
        best_makespan,best_citizen_idx = pop_w_makespan[0]
        self.best_permutation_with_makespan.append((self.population[best_citizen_idx], best_makespan))

        # create distribution values
        distr_ind = []
        distr = []
        for i in range(self.n_pop):
            distr_ind.append(pop_w_makespan[i][1])
            distr.append((2*(i+1)) / (self.n_pop * (self.n_pop+1)))


        # select parents (for each new child there are 2 parents)
        for i in range(self.n_pop):
            self.parents.append(list(choice(distr_ind, 2, p=distr)))
    
    def __crossover(self) -> None:
        """ Apply crossover.
            Create and fill out self.children list """

        self.children = []

        for p in self.parents:
            r = random.random()
            if r < self.p_cross:
                self.children.append(crossover.ordered_crossover(self.population[p[0]], self.population[p[1]])) 
            else:
                if r < 0.5:
                    self.children.append(self.population[p[0]])
                else:
                    self.children.append(self.population[p[1]])
        
    def __mutation(self):
        """ Apply mutation.
            Affects self.children list"""

        logging.debug("Starting mutation.")
        for c in self.children:
            r = random.random()
            if r < self.p_mut:
                c = mutation.mutation(c)
        logging.debug("Mutation finished.")
 
    def __elitist_update(self):
        """ Add best specimen from previous population (self.population)
            instead of a random one from the children (self.children)
            Affects self.children list """

        logging.debug("Starting elitist update.")
        
        # initialize
        best_makespan, best_parent_idx = Inf, -1
        worst_makespan = 0
        average_makespan = 0
        
        # Get best specimen from old population
        for i, p in enumerate(self.population):
            temp_makespan = self.calculate_makespan(p)
            if temp_makespan < best_makespan:
                best_parent_idx = i
                best_makespan = temp_makespan

            # check for worst makespan
            if worst_makespan < temp_makespan:
                worst_makespan = temp_makespan

            # collect data for avg makespan
            average_makespan += temp_makespan

        # calculate avg_makespan
        average_makespan = average_makespan / self.n_pop

        # print out the best specimen
        # logging.info(f"Makespan of the best specimen from the current population: {best_makespan}")
        self.best_specimen.append(best_makespan)
        self.worst_specimen.append(worst_makespan)
        self.average_specimen.append(average_makespan)

        # Substitue random child with best parent
        random_idx = random.randint(0, self.n_pop - 1)
        self.children[random_idx] = self.population[best_parent_idx]

        logging.debug("Elitist update finished.")

    def __grow_children(self):
        """ Kill parents (self.population) and make children the new parents
            Affects self.population list """

        self.population = self.children

    def run(self):
        """Run the algorithm for 'n_epoch' times"""
        for i in range(self.n_epoch):
            
            if (i%500==0):
                print(f"iter: {i}/{self.n_epoch}; {i/self.n_epoch*100}%")

            # Selecting parents for breeding
            self.__selection()
            
            # Create offspring from parents by crossover
            self.__crossover()

            # Mutate offspring
            self.__mutation()

            # elitist update - bring few best from the previous iteration
            self.__elitist_update()

            # kill parents (pupulation). Make children the new parents (population).
            self.__grow_children()

        return
    
    def plot(self):
        """ Plots progress """

        fig, ax = plt.subplots()
        ax.set(xlabel='Generation', ylabel='Makespan',
            title='Genetic Flow Shop')
        ax.plot(range(0, self.n_epoch), self.best_specimen)
        ax.grid()

        if not os.path.exists("./results/"):
            os.mkdir("./results/")
            
        fig.savefig("./results/test.png")

        plt.show()



if __name__ == "__main__":


    
    
    logging.info("I'm an informational message.")
    logging.debug("I'm a message for debugging purposes.")
    logging.warning("I'm a warning. Beware!")
    """
    ● DEBUG: You should use this level for debugging purposes in development.
    ● INFO: You should use this level when something interesting—but expected—happens (e.g., a user starts a new project in a project management application).
    ● WARNING: You should use this level when something unexpected or unusual happens. It’s not an error, but you should pay attention to it.
    ● ERROR: This level is for things that go wrong but are usually recoverable (e.g., internal exceptions you can handle or APIs returning error results).
    ● CRITICAL: You should use this level in a doomsday scenario. The application is unusable. At this level, someone should be woken up at 2 a.m.
    """

    # Number of population
    n_pop = 4
    # Probability of crossover
    p_cross = 0.90
    # Probability of mutation
    p_mut = 0.80
    # Stopping number for generation
    n_epoch = 100
    # Number of machines and tasks
    n, m = 4, 3

    # Read operation times
    operation_times = read_operations(n, m)

    # Run single iteration
    gfs = GeneticFlowShop(  m, n, operation_times, 
                            n_pop, p_cross, p_mut, n_epoch)
    t1 = time.process_time() # Start Timer
    gfs.run()
    t2 = time.process_time() # Stop Timer
    gfs.plot()
    # plt.show(block=True)

    print("CPU Time (s)")
    timePassed = (t2-t1)
    print("%.2f" %timePassed)