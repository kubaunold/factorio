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
            [5, 10, 6,  8],
            [8, 15, 5,  7],
            [8, 5,  7,  9],
        ]

        self.num_machines = len(self.duration)
        self.num_jobs = len(self.duration[0])
        self.time_start = zeros((self.num_machines, self.num_jobs), dtype=int)
        self.makespan = Inf
        self.permutation = [0, 1, 2, 3]
        self.schedule = []

        for m in range(self.num_machines):
            for n in range(self.num_jobs):
                print(f"{m=}{n=}")
                # o = Operation(duration=self.op[m][n], machine_number=m, job_number=n)
                # self.schedule.append(o)

                    # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
                    # poprzednik kolejnościowy - inne zadanie z tej samej maszyny

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

        print(f"{self.time_start=}")

    def __repr__(self) -> str:
        return f"My operations: {self.duration}"
        



    def calculate_makespan(self):
        return 20




def main():
    fs = FlowShop()
    print(f"Hello world! {fs}")
    i = 2

if __name__ == '__main__':
    main()
