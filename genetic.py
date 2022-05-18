import random
import time
from numpy.random import permutation, choice
from app import FlowShop
from util import read_operations, silnia


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
        self.parents = []
        self.children = []
        # print(f"{self.population=}")

    def __get_initial_population(self):
        """Creating the initial population (n_pop distinct chromosomes)"""

        pop = []
        allow_duplicate = False

        if self.n_pop > silnia(self.m):
            print("Warning! Size of the population exceeds number of possible permutations.py. There will be duplicate permutations.")
            allow_duplicate = True

        for i in range(self.n_pop):
            """Select specimen one by one"""
            p = list(permutation(self.n))
            if allow_duplicate:
                p = list(permutation(self.n))
            else:
                while p in pop:
                    p = list(permutation(self.n))
            print(f"num_citizens={len(pop)}")

            pop.append(p)


        return pop

    def __selection(self) -> None:
        """Select parents based on given population
            Updates self.parents list"""

        # purge parents
        self.parents = []

        # create list of tuples such as: (makespan, index)
        pop_w_makespan = []
        for i in range(self.n_pop):
            pop_w_makespan.append([self.calculate_makespan(self.population[i]), i]) 

        print(pop_w_makespan)

        # sort by ascending value makespan (the fittest is at the beginning)
        pop_w_makespan.sort()
        print(f"Pop_w_makespan after sort= {pop_w_makespan}")


        # create distribution values
        distr_ind = []
        distr = []
        for i in range(self.n_pop):
            distr_ind.append(pop_w_makespan[i][1])
            distr.append((2*(i+1)) / (self.n_pop * (self.n_pop+1)))

        print(f"{distr_ind = }")
        print(f"{distr = }")

        # select parents (for each new child there are 2 parents)
        for i in range(self.n_pop):
            self.parents.append(list(choice(distr_ind, 2, p=distr)))
        print(f"{self.parents = }")
    
    def __crossover(self) -> None:
        """Apply crossover
            Updates self.children"""
        for p in self.parents:
            r = random.random()
            if r < self.p_cross:
                
                
                self.children.append(self.population[p[0]])
                # here some crossing needs to be done
                pass
                # self.population.append(crossover([population[p[0]], population[p[1]]]))
            else:
                if r < 0.5:
                    self.children.append(self.population[p[0]])
                else:
                    self.children.append(self.population[p[1]])
        

        print(self.children)


    def run(self):
        """Run the algorithm for 'n_iter' times"""
        for i in range(self.n_iter):
            
            # Selecting parents
            self.__selection()
            
            # apply crossover
            self.__crossover()


        
        
        return


            
        #     # Apply mutation 
        #     for c in childs:
        #         r = random.random()
        #         if r < Pm:
        #             c = mutation(c)

        #     # Update the population
        #     population = elitistUpdate(population, childs)
            
        #     #print(population)
        #     #print(findBestSolution(population))







if __name__ == "__main__":
    # Number of population
    n_pop = 4
    # Probability of crossover
    p_cross = 1.0
    # Probability of mutation
    p_mut = 1.0
    # Stopping number for generation
    n_iter = 1


    m, n = 5, 7
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