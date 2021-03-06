"""
Application performing creating a schedule for Permutation-FlowShop `F*` (all machines have the same sequence).
It then calculates makespan for some random permutation of jobs and displays the result on a gantt chart.

Steps:
1) Read operation times into a Matrix
2) Select permutation of jobs
3) Calculate makespan
4) Display gantt chart
"""

from cmath import inf
from numpy import zeros
from gantt_fs import create_and_show_gantt_fs
from util import get_machine_names, get_task_names, read_operations, sum_of_list

class FlowShop:
    """Object for solving FlowShop problem"""
    
    def __init__(self, m, n, operation_times) -> None:
        # self.op_times = [
        #     [4, 4, 2, 3],
        #     [3, 1, 1, 2],
        #     [4, 1, 2, 1],
        # ]
        self.op_times = operation_times     # duration of every operation
        self.m = len(self.op_times)         # number of machines
        self.n = len(self.op_times[0])      # number of machines
        self.start_times = zeros((self.m, self.n), dtype=int)    # matrix with operation start times

        # Run some health checks
        if(m == len(self.op_times)):
            self.m = len(self.op_times)     # number of machines
        else:
            raise NameError("Number of machines does not match")

        if(n == len(self.op_times[0])):
            self.n = len(self.op_times[0])     # number of machines
        else:
            raise NameError("Number of tasks does not match")

        # self.cmax = Inf                      # makespan
        # self.pi = [3, 1, 0, 2]               # permutation
        # self.solution = (pi, cmax)      # solution is a tuple of permutation and its makespan
        


    def __repr__(self) -> str:
        return f"My operations: {self.op_times}"
    
    def calculate_makespan(self, permutation) -> int:
        """ Calculates makespan for a given permutation """
        for m in range(self.m):
            for n in range(self.n):
                # technological ancestor finish - finish time of an operation that's a tech predecessor
                # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
                taf = self.__technological_ancestor_finish(permutation, m, n)
                # order ancestor finish - finish time of an operation that's an oredr predecessor
                # poprzednik kolejno??ciowy - inne zadanie z tej samej maszyny
                maf = self.__machine_ancestor_finish(permutation, m, n)
                # operation starts on later of these two
                self.start_times[m][permutation[n]] = max(taf, maf)

        return self.start_times[-1][permutation[-1]] + self.op_times[-1][permutation[-1]]

    def __technological_ancestor_finish(self, permutation, m, n) -> int:
        """Calculates finish time of an operation, that's a technological predecessor
        to operation[m][n]"""
        if m == 0 and n == 0:
            return 0
        elif m != 0 and n == 0:
            return self.start_times[m-1][permutation[n]] + self.op_times[m-1][permutation[n]]
        elif m == 0 and n != 0:
            return 0
        elif m != 0 and n != 0:
            return self.start_times[m-1][permutation[n]] + self.op_times[m-1][permutation[n]]

    def __machine_ancestor_finish(self, permutation, m, n) -> int:
        """Calculates finish time of an operation, that's an order predecessor
        to operation[m][n]"""
        if m == 0 and n == 0:
            return 0
        elif m != 0 and n == 0:
            return 0
        elif m == 0 and n != 0:
            return self.start_times[m][permutation[n-1]] + self.op_times[m][permutation[n-1]]
        elif m != 0 and n != 0:
            return self.start_times[m][permutation[n-1]] + self.op_times[m][permutation[n-1]]

    def get_schedule(self) -> list[dict]:
        """ Creates schedule - list of dicts for every operation containing its start time and duration
            for the purpose of Gantt diagram visualization """

        def add_subtask(schedule, t0, d, i_maq, i_tarea):
            # Dict of a subtask
            subtask = {'t0': t0, 'd': d, 'i_machine': i_maq, 'i_task': i_tarea}

            # Add to schedule
            schedule.append(subtask)
        
        schedule = []

        for m in range(self.m):
            for n in range(self.n):
                add_subtask(schedule, self.start_times[m][n], self.op_times[m][n], m, n)

        return schedule

def main():
    n, m = 20, 5
    operation_times = read_operations(n, m)
    fs = FlowShop(m=m, n=n, operation_times=operation_times)
    
    import itertools
    all_perms = []
    # all_perms = list(itertools.permutations(list(i for i in range(n))))
    optim_perm = [3, 17,	15,	8,	9,	6,	5,	14,	16,	7,	11,	13,	18,	19,	1,	4,	2,	10,	20,	12]
    optim_perm_idxs = [x-1 for x in optim_perm]
    all_perms.append(optim_perm_idxs)
    best_makespan = inf
    best_permutation = []
    best_schedule = []
    makespan_list = []
    
    for permutation in all_perms:
        makespan = fs.calculate_makespan(permutation)
        schedule = fs.get_schedule()

        if makespan < best_makespan:
            best_makespan = makespan
            best_permutation = permutation
            best_schedule = schedule
            makespan_list.append(makespan)
        
        # create_and_show_gantt_fs(schedule, machine_names, job_names)

        machine_names = get_machine_names(m)
        job_names = get_task_names(n)
    create_and_show_gantt_fs(best_schedule, machine_names, job_names)




if __name__ == '__main__':
    main()
