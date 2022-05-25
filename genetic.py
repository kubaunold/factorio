from distutils.debug import DEBUG
import random
from re import I
import time
from numpy import Inf
from numpy.random import permutation, choice
from app import FlowShop
from util import read_operations, silnia
import mutation, crossover
from base_logger import logger as logging

def calculateObj(sol):
    qTime = queue.PriorityQueue()
    
    qMachines = []
    for i in range(m):
        qMachines.append(queue.Queue())
    
    for i in range(n):
        qMachines[0].put(sol[i])
    
    busyMachines = []
    for i in range(m):
        busyMachines.append(False)
    
    time = 0
    
    job = qMachines[0].get()
    qTime.put((time+cost[job][0], 0, job))
    busyMachines[0] = True
    
    while True:
        time, mach, job = qTime.get()
        if job == sol[n-1] and mach == m-1:
            break
        busyMachines[mach] = False
        if not qMachines[mach].empty():
                j = qMachines[mach].get()
                qTime.put((time+cost[j][mach], mach, j))
                busyMachines[mach] = True
        if mach < m-1:
            if busyMachines[mach+1] == False:
                qTime.put((time+cost[job][mach+1], mach+1, job))
                busyMachines[mach+1] = True
            else:
                qMachines[mach+1].put(job)
            
    return time

def selection(pop):
    popObj = []
    for i in range(len(pop)):
        popObj.append([calculateObj(pop[i]), i])
    
    popObj.sort()
    
    distr = []
    distrInd = []
    
    for i in range(len(pop)):
        distrInd.append(popObj[i][1])
        prob = (2*(i+1)) / (len(pop) * (len(pop)+1))
        distr.append(prob)
    
    parents = []
    for i in range(len(pop)):
        parents.append(list(np.random.choice(distrInd, 2, p=distr)))
    
    return parents



class GeneticFlowShop(FlowShop):
    def __init__(self, m, n, operation_times, n_pop, p_cross, p_mut, n_iter) -> list:
        super().__init__(m, n, operation_times)
        self.n_pop = n_pop
        self.p_cross = p_cross
        self.p_mut = p_mut
        self.n_iter = n_iter
        
        self.population = self.__get_initial_population()

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
        
        # Get best specimen from old population
        for i, p in enumerate(self.population):
            temp_makespan = self.calculate_makespan(p)
            if temp_makespan < best_makespan:
                best_parent_idx = i
                best_makespan = temp_makespan

        # print out the best specimen
        logging.info(f"Makespan of the best specimen from the current population: {best_makespan}")

        # Substitue random child with best parent
        random_idx = random.randint(0, self.n_pop - 1)
        self.children[random_idx] = self.population[best_parent_idx]

        logging.debug("Elitist update finished.")

    def __grow_children(self):
        """ Kill parents (self.population) and make children the new parents
            Affects self.population list """

        self.population = self.children

    def run(self):
        """Run the algorithm for 'n_iter' times"""
        for i in range(self.n_iter):
            
            # Selecting parents for breeding
            self.__selection()
            
            # Create offspring from parents by crossover
            self.__crossover()

            # Mutate offspring
            self.__mutation()

            # elitist update - bring few best from the previous iteration
            self.__elitist_update()

            logging.info(f"Iter[{i}]: makespan of 1st child: {self.calculate_makespan(self.children[0])}")
 
            # kill parents (pupulation). Make children the new parents (population).
            self.__grow_children()

        
        return





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
    p_cross = 1.0
    # Probability of mutation
    p_mut = 1.0
    # Stopping number for generation
    n_iter = 1000


    m, n = 5, 20
    operation_times = read_operations(m, n)

    gfs = GeneticFlowShop(  m, n, operation_times, 
                            n_pop, p_cross, p_mut, n_iter)

    # Start Timer
    t1 = time.process_time()
    gfs.run()





    # Stop Timer
    t2 = time.process_time()
        
    # # Results Time

    # bestSol, bestObj, avgObj = findBestSolution(population)
        
    # print("Population:")
    # print(population)
    # print() 

    # print("Solution:")
    # print(population[bestSol])
    # print() 

    # print("Objective Value:")
    # print(bestObj)
    # print()

    # print("Average Objective Value of Population:")
    # print("%.2f" %avgObj)
    # print()

    # print("%Gap:")
    # G = 100 * (bestObj-optimalObjective) / optimalObjective
    # print("%.2f" %G)
    # print()

    print("CPU Time (s)")
    timePassed = (t2-t1)
    print("%.2f" %timePassed)