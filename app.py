"""
Application performing creating a schedule for Permutation-FlowShop `F*` (all machines have the same sequence).
It then calculates makespan for some random permutation of jobs and displays the result on a gantt chart.

Steps:
1) Read operation times into a Matrix
2) Select permutation of jobs
3) Calculate makespan
4) Display gantt chart
"""

from numpy import Inf, zeros
from ..flowshop.flow_shop_intro.gantt_fs import crear_y_mostrar_gantt_fs



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
    
    def __init__(self) -> None:
        self.duration = [
            [4, 4, 2,  3],
            [3, 1, 1,  2],
            [4, 1,  2,  1],
        ]

        self.m = len(self.duration)     # number of machines
        self.n = len(self.duration[0])  # number of tasks
        self.time_start = zeros((self.m, self.n), dtype=int)    # matrix with operation start times
        
        cmax = Inf                      # makespan
        pi = [3, 1, 0, 2]               # permutation
        self.solution = (pi, cmax)      # solution is a tuple of permutation and its makespan
        
        print(f"FlowShop object created")

    def __repr__(self) -> str:
        return f"My operations: {self.duration}"
    
    def calculate_makespan(self, permutation) -> int:
        self.permutation = permutation

        for m in range(self.m):
            for n in range(self.n):

                # technological ancestor finish - finish time of an operation that's a tech predecessor
                # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
                taf = self.technological_ancestor_finish(permutation, m, n)
                # order ancestor finish - finish time of an operation that's an oredr predecessor
                # poprzednik kolejnościowy - inne zadanie z tej samej maszyny
                oaf = order_ancestor_finish()

                if m == 0 and n == 0:
                    ancestor_tech_finish = 0
                    ancestor_order_finish = 0
                elif m != 0 and n == 0:
                    ancestor_tech_finish = self.time_start[m-1][n] + self.duration[m-1][n]
                    ancestor_order_finish = 0
                elif m == 0 and n != 0:
                    ancestor_tech_finish = 0
                    ancestor_order_finish = self.time_start[m][n-1] + self.duration[m][n-1]
                elif m != 0 and n != 0:

                    ancestor_tech_finish = self.time_start[m-1][n] + self.duration[m-1][n]
                    ancestor_order_finish = self.time_start[m][n-1] + self.duration[m][n-1]

                self.time_start[m][n] = max(ancestor_tech_finish, ancestor_order_finish)

        return 100

    def technological_ancestor_finish(self, m, n):
        if m == 0 and n == 0:
            return 0 + self.duration[m][n]
        elif m != 0 and n == 0:
            return self.time_start[]
            ancestor_tech_finish = self.time_start[m-1][n] + self.duration[m-1][n]
            ancestor_order_finish = 0
        elif m == 0 and n != 0:
            ancestor_tech_finish = 0
            ancestor_order_finish = self.time_start[m][n-1] + self.duration[m][n-1]
        elif m != 0 and n != 0:
            ancestor_tech_finish = self.time_start[m-1][n] + self.duration[m-1][n]
            ancestor_order_finish = self.time_start[m][n-1] + self.duration[m][n-1]

        return taf


    def show_gantt(self):
        
        def add_subtask(schedule, t0, d, i_maq, i_tarea):
            # Dict of a subtask
            subtask = {'t0': t0, 'd': d, 'i_maq': i_maq, 'i_tarea': i_tarea}

            # Add to schedule
            schedule.append(subtask)
        
        schedule = []




def main():
    fs = FlowShop()
    print(f"Hello world! {fs}")
    i = 2

if __name__ == '__main__':
    main()
