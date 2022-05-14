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
from numpy import Inf, zeros
from gantt_fs import crear_y_mostrar_gantt_fs
from time import sleep
from util import read_operations

class Operation:
    """Most atomic cell of a FlowShop problem"""

    def __init__(self, duration=None, start=None, finish=None, machine_number=None, job_number=None) -> None:
        self.duration = duration
        self.start = start
        self.finish = finish
        self.machine_number = machine_number
        self.job_number = job_number

    def __repr__(self) -> str:
        return f"op[{self.machine_number}][{self.job_number}]=[{self.duration}]"


class FlowShop:
    """Object for solving FlowShop problem"""
    
    def __init__(self, m, n, operation_times) -> None:
        # self.duration = [
        #     [4, 4, 2, 3],
        #     [3, 1, 1, 2],
        #     [4, 1, 2, 1],
        # ]
        self.duration = operation_times

        if(m == len(self.duration)):
            self.m = len(self.duration)     # number of machines
        else:
            raise NameError("Number of machines does not match")

        if(n == len(self.duration[0])):
            self.n = len(self.duration[0])     # number of machines
        else:
            raise NameError("Number of tasks does not match")


        self.time_start = zeros((self.m, self.n), dtype=int)    # matrix with operation start times
        
        # self.cmax = Inf                      # makespan
        # self.pi = [3, 1, 0, 2]               # permutation
        # self.solution = (pi, cmax)      # solution is a tuple of permutation and its makespan
        
        print(f"FlowShop object created")

    def __repr__(self) -> str:
        return f"My operations: {self.duration}"
    
    def calculate_makespan(self, permutation) -> int:

        for m in range(self.m):
            for n in range(self.n):
                # technological ancestor finish - finish time of an operation that's a tech predecessor
                # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
                taf = self.technological_ancestor_finish(permutation, m, n)
                # order ancestor finish - finish time of an operation that's an oredr predecessor
                # poprzednik kolejnościowy - inne zadanie z tej samej maszyny
                oaf = self.order_ancestor_finish(permutation, m, n)
                # operation starts on later of these two
                self.time_start[m][permutation[n]] = max(taf, oaf)

        return self.time_start[-1][permutation[-1]] + self.duration[-1][permutation[-1]]

    def technological_ancestor_finish(self, permutation, m, n) -> int:
        """Calculates finish time of an operation, that's a technological predecessor
        to operation[m][n]"""
        if m == 0 and n == 0:
            return 0
        elif m != 0 and n == 0:
            return self.time_start[m-1][permutation[n]] + self.duration[m-1][permutation[n]]
        elif m == 0 and n != 0:
            return 0
        elif m != 0 and n != 0:
            return self.time_start[m-1][permutation[n]] + self.duration[m-1][permutation[n]]

    def order_ancestor_finish(self, permutation, m, n) -> int:
        """Calculates finish time of an operation, that's an order predecessor
        to operation[m][n]"""
        if m == 0 and n == 0:
            return 0
        elif m != 0 and n == 0:
            return 0
        elif m == 0 and n != 0:
            return self.time_start[m][permutation[n-1]] + self.duration[m][permutation[n-1]]
        elif m != 0 and n != 0:
            return self.time_start[m][permutation[n-1]] + self.duration[m][permutation[n-1]]

    def get_schedule(self):
        """Creates schedule - dict with task duration and start times"""
        def add_subtask(schedule, t0, d, i_maq, i_tarea):
            # Dict of a subtask
            subtask = {'t0': t0, 'd': d, 'i_machine': i_maq, 'i_task': i_tarea}

            # Add to schedule
            schedule.append(subtask)
        
        schedule = []

        for m in range(self.m):
            for n in range(self.n):
                add_subtask(schedule, self.time_start[m][n], self.duration[m][n], m, n)

        return schedule






def main():
    m, n = 5, 7
    operation_times = read_operations(m, n)
    fs = FlowShop(m=m, n=n, operation_times=operation_times)
    
    import itertools
    all_permms = list(itertools.permutations(list(i for i in range(n))))
    

    best_makespan = inf
    best_permutation = []
    best_schedule = []
    makespan_list = []
    
    for permutation in all_permms:
        makespan = fs.calculate_makespan(permutation)
        schedule = fs.get_schedule()

        print(f"{schedule=}")

        if makespan < best_makespan:
            best_makespan = makespan
            best_permutation = permutation
            best_schedule = schedule
            makespan_list.append(makespan)
        
        # crear_y_mostrar_gantt_fs(schedule, machine_names, job_names)

    machine_names = ["M0", "M1", "M2", "M3", "M4"]
    job_names = ["T0", "T1", "T2", "T3", "T4", "T5", "T6"]
    print(f"{best_makespan=}")
    print(f"{best_permutation=}")
    crear_y_mostrar_gantt_fs(schedule, machine_names, job_names)
    print(f"{makespan_list=}")


if __name__ == '__main__':
    main()
