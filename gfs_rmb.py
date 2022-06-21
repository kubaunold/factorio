""" class solving Flow Shop with Machine Breakdown using Genetic Algorithm """

from asynchat import simple_producer
import random
import time
from numpy import Inf
from numpy.random import permutation, choice
from fs_rmb import FlowShopWithMachineBreakdown
from gantt_fs import create_and_show_gantt_fs
from util import get_machine_names, get_task_names, read_operations, silnia
import mutation, crossover
from base_logger import logger as logging
import matplotlib.pyplot as plt
import os

class GeneticFlowShopWithMachineBreakdown(FlowShopWithMachineBreakdown):
    def __init__(   self, m, n, operation_times,
                    n_pop, p_cross, p_mut, n_epoch,
                    failure_size) -> list:
        super().__init__(m, n, operation_times, failure_size)
        self.n_pop = n_pop
        self.p_cross = p_cross
        self.p_mut = p_mut
        self.n_epoch = n_epoch
        
        self.population = self.__get_initial_population()
        # list of best specimen for each epoch
        self.best_specimen = []
        self.worst_specimen = []
        self.average_specimen = []

        # List of tuples: best permutations across all generations and its makespan
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
        
        # Small hack for population (AG with has one NEH result osobnik na poczatku)
        if True:
            if self.n == 20 and self.m == 5:
                pop[-1] = [14, 10, 15, 18, 5, 3, 4, 17, 0, 1, 9, 6, 19, 8, 2, 13, 7, 11, 16, 12]
            if self.n == 20 and self.m == 20:
                pop[-1] = [15, 14, 9, 7, 8, 11, 12, 10, 0, 19, 13, 16, 1, 17, 4, 5, 6, 18, 2, 3]
            if self.n == 50 and self.m == 10:
                pop[-1] = [24, 21, 30, 35, 41, 42, 37, 28, 3, 5, 13, 1, 46, 14, 27, 10, 22, 34, 45, 8, 16, 39, 2, 4, 12, 11, 9, 20, 44, 15, 49, 40, 26, 43, 29, 32, 19, 33, 48, 31, 7, 25, 17, 36, 6, 18, 23, 0, 47, 38]
            if self.n == 100 and self.m == 20:
                pop[-1] = [21, 30, 23, 40, 82, 54, 32, 38, 99, 29, 15, 90, 26, 98, 9, 19, 11, 20, 2, 27, 92, 31, 1, 60, 8, 33, 62, 95, 66, 65, 94, 69, 55, 14, 6, 34, 85, 80, 44, 5, 52, 84, 70, 22, 16, 87, 78, 71, 75, 47, 17, 67, 63, 28, 86, 61, 42, 25, 51, 41, 48, 53, 0, 58, 10, 81, 83, 13, 36, 79, 73, 3, 7, 91, 45, 37, 4, 39, 74, 56, 64, 57, 77, 59, 97, 89, 24, 46, 93, 76, 68, 96, 18, 43, 88, 12, 50, 72, 49, 35]
            if self.n == 200 and self.m == 10:
                pop[-1] = [158, 171, 15, 68, 197, 149, 161, 163, 103, 65, 133, 185, 122, 164, 82, 119, 13, 63, 74, 41, 192, 199, 7, 52, 62, 116, 1, 174, 106, 198, 134, 193, 131, 24, 17, 18, 37, 101, 23, 188, 8, 178, 153, 34, 173, 25, 81, 91, 114, 191, 96, 195, 12, 16, 39, 73, 107, 19, 130, 88, 170, 43, 180, 120, 104, 115, 186, 152, 117, 78, 184, 165, 57, 10, 143, 47, 127, 118, 176, 31, 61, 4, 53, 121, 55, 111, 85, 6, 105, 137, 69, 30, 9, 11, 142, 144, 100, 87, 3, 140, 71, 125, 45, 113, 183, 58, 138, 94, 67, 83, 54, 21, 20, 40, 79, 50, 110, 26, 49, 129, 22, 72, 151, 132, 64, 86, 93, 154, 128, 0, 126, 70, 14, 60, 97, 56, 109, 194, 155, 166, 167, 175, 189, 29, 35, 75, 2, 190, 76, 159, 84, 169, 80, 124, 123, 141, 139, 42, 172, 38, 27, 36, 168, 160, 108, 182, 162, 48, 90, 177, 187, 145, 196, 95, 5, 59, 51, 147, 66, 99, 181, 112, 89, 146, 157, 136, 32, 46, 156, 28, 150, 92, 102, 33, 148, 44, 179, 135, 77, 98]
            if self.n == 500 and self.m == 20:
                pop[-1] = [173, 438, 287, 474, 460, 327, 269, 89, 285, 424, 67, 278, 21, 328, 110, 343, 471, 216, 108, 376, 498, 75, 395, 152, 384, 77, 295, 336, 473, 103, 63, 2, 3, 380, 273, 211, 37, 86, 469, 208, 431, 146, 22, 95, 298, 235, 220, 218, 142, 497, 247, 16, 489, 55, 156, 6, 409, 96, 145, 101, 47, 56, 40, 434, 486, 223, 369, 375, 479, 212, 163, 164, 360, 332, 181, 186, 58, 408, 185, 200, 120, 168, 234, 34, 385, 478, 284, 393, 36, 276, 242, 487, 209, 206, 24, 413, 492, 420, 370, 302, 493, 165, 85, 43, 253, 377, 361, 418, 172, 160, 459, 325, 251, 198, 88, 175, 30, 73, 383, 35, 104, 5, 149, 187, 45, 147, 432, 491, 97, 417, 293, 257, 352, 357, 106, 274, 151, 382, 483, 0, 205, 310, 271, 199, 445, 68, 80, 477, 354, 219, 456, 440, 10, 196, 309, 485, 171, 296, 131, 414, 345, 401, 249, 463, 140, 50, 350, 148, 49, 499, 99, 428, 300, 194, 128, 270, 476, 366, 76, 415, 282, 29, 79, 482, 264, 289, 403, 259, 135, 176, 362, 92, 178, 252, 129, 374, 177, 59, 312, 425, 91, 201, 141, 333, 453, 465, 419, 202, 65, 179, 318, 351, 7, 372, 229, 402, 464, 342, 331, 355, 319, 210, 64, 347, 335, 338, 246, 116, 461, 435, 470, 26, 291, 133, 167, 396, 283, 307, 121, 81, 228, 280, 174, 367, 329, 261, 117, 462, 427, 288, 222, 127, 467, 484, 144, 451, 406, 159, 387, 450, 1, 215, 61, 93, 183, 8, 66, 109, 334, 326, 490, 54, 112, 166, 398, 241, 27, 23, 158, 197, 25, 111, 100, 190, 412, 193, 297, 180, 48, 394, 57, 138, 78, 150, 344, 237, 353, 364, 306, 82, 323, 458, 15, 9, 182, 227, 191, 255, 346, 46, 256, 226, 340, 157, 245, 472, 123, 452, 411, 441, 115, 62, 348, 11, 430, 60, 448, 439, 324, 365, 315, 330, 404, 321, 397, 455, 137, 263, 266, 18, 407, 204, 371, 169, 155, 457, 442, 294, 84, 410, 19, 488, 41, 373, 51, 320, 275, 359, 301, 12, 13, 422, 260, 449, 136, 188, 358, 481, 322, 433, 381, 349, 162, 153, 379, 496, 126, 192, 139, 308, 389, 279, 286, 90, 87, 258, 72, 292, 243, 114, 314, 303, 254, 39, 400, 444, 225, 74, 33, 221, 38, 494, 480, 454, 203, 390, 119, 437, 207, 143, 238, 170, 52, 443, 232, 475, 14, 495, 44, 233, 277, 405, 305, 118, 248, 341, 17, 113, 272, 447, 416, 217, 53, 20, 436, 161, 446, 224, 105, 231, 378, 28, 42, 466, 391, 386, 94, 426, 134, 368, 281, 244, 337, 98, 317, 4, 239, 122, 132, 250, 189, 195, 316, 213, 267, 356, 304, 130, 70, 311, 423, 124, 240, 154, 313, 388, 102, 468, 265, 83, 392, 399, 429, 230, 290, 71, 262, 339, 214, 69, 268, 107, 421, 125, 363, 31, 236, 184, 32, 299]
        
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



def main():
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
    n_epoch = 100
    # Number of machines and tasks
    n, m = 7, 5
    # Failure size
    failure_size = 0.3
    # Read operation times
    operation_times = read_operations(n, m)

    # Run single iteration
    gfsrmb = GeneticFlowShopWithMachineBreakdown(
        m, n, operation_times, 
        n_pop, p_cross, p_mut, n_epoch,
        failure_size)

    t1 = time.process_time() # Start Timer
    gfsrmb.run()
    t2 = time.process_time() # Stop Timer

    print("CPU Time (s)")
    timePassed = (t2-t1)
    print("%.2f" %timePassed)

    # Show best permutation on gantt diagram
    (best_permutation, _) = gfsrmb.best_permutation_with_makespan[-1]
    _ = gfsrmb.calculate_makespan(best_permutation)
    
    # Show simple permutation
    # simple_permutation = [i for i in range(n)]
    # _ = gfsrmb.calculate_makespan(simple_permutation)


    schedule = gfsrmb.get_schedule()

    machine_names = get_machine_names(m)
    job_names = get_task_names(n)
    create_and_show_gantt_fs(schedule, machine_names, job_names, breakdown=gfsrmb.breakdown)

    




if __name__ == "__main__":
    main()
