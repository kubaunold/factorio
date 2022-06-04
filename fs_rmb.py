"""
Module implementing FlowShop problem with additional Random Machine Breakdown, meaning
that there will be a certain machine unavailable for given period of time.
"""

from cmath import inf
from random import randint
import random
from numpy import Inf, zeros
from breakdown import Breakdown
from fs import FlowShop
from gantt_fs import create_and_show_gantt_fs
from time import sleep
from util import get_machine_names, get_task_names, read_operations, sum_of_list

class FlowShopWithMachineBreakdown(FlowShop):
    def __init__(self, m, n, operation_times, failure_size) -> None:
        super().__init__(m, n, operation_times)

        self.failure_size = failure_size
        self.breakdown = self.__generate_breakdown()

    def __generate_breakdown(self):
        """ Generates breakdown based on failure_size param """
        makespan = sum_of_list(self.op_times[0])
        random.seed(10)     # TEMPORAL: unrandomize things
        breakdown_duration = max(randint(5,15), int(makespan * self.failure_size))
        return Breakdown(randint(0,self.m - 1), randint(0, makespan), breakdown_duration)

    def calculate_makespan(self, permutation) -> int:
        for m in range(self.m):
            for n in range(self.n):
                # technological ancestor finish - finish time of an operation that's a tech predecessor
                # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
                taf = self._FlowShop__technological_ancestor_finish(permutation, m, n)
                # machine ancestor finish - finish time of an operation that's an oredr predecessor
                # poprzednik kolejnościowy - inne zadanie z tej samej maszyny
                maf = self._FlowShop__machine_ancestor_finish(permutation, m, n)
                
                # start time is the later of these two
                start_time = max(taf, maf)


                if m == self.breakdown.m:
                    # does the machine breakdown occur?
                    if (start_time + self.start_times[m][permutation[n]]) < self.breakdown.t0:
                        # will this op have enough time to finish before the breakdown start?
                        self.start_times[m][permutation[n]] = start_time
                    else:
                        # insert it right after the machine gets fixed
                        self.start_times[m][permutation[n]] = self.breakdown.t0 + self.breakdown.breakdown_duration

    def plot_sample(self):
        _ = self.calculate_makespan([0,2,1,3])
        some_schedule = self.get_schedule()

        machine_names = get_machine_names(self.m)
        job_names = get_task_names(self.n)
        create_and_show_gantt_fs(some_schedule, machine_names, job_names, breakdown=self.breakdown)



def main():

    m, n = 3, 4
    operation_times = read_operations(m, n)
    failure_size = 0.03
    fs_rmb = FlowShopWithMachineBreakdown(m, n, operation_times, failure_size)
    fs_rmb.plot_sample()


if __name__ == '__main__':
    main()
