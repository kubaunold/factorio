"""
Module implementing FlowShop problem with additional Random Machine Breakdown, meaning
that there will be a certain machine unavailable for given period of time.
"""

from random import randint
import random
from breakdown import Breakdown
from fs import FlowShop
from gantt_fs import create_and_show_gantt_fs
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
                    # there is a breakdown
                    if (start_time + self.op_times[m][permutation[n]]) <= self.breakdown.t0:
                        # op will finish before the breakdown start
                        self.start_times[m][permutation[n]] = start_time
                    else:
                        # op has to start after
                        self.start_times[m][permutation[n]] = max(start_time, self.breakdown.t0 + self.breakdown.breakdown_duration)
                else:
                    # there is no breakdown on this machine
                    self.start_times[m][permutation[n]] = start_time

        return self.start_times[-1][permutation[-1]] + self.op_times[-1][permutation[-1]]


    def plot_sample(self):
        _ = self.calculate_makespan([0,2,1,3])
        some_schedule = self.get_schedule()

        machine_names = get_machine_names(self.m)
        job_names = get_task_names(self.n)
        create_and_show_gantt_fs(some_schedule, machine_names, job_names, breakdown=self.breakdown)



def main():

    # n, m = 4, 3
    # neh_perm = [2, 0, 3, 1]

    # n, m = 20, 5
    # neh_perm = [14, 10, 15, 18, 5, 3, 4, 17, 0, 1, 9, 6, 19, 8, 2, 13, 7, 11, 16, 12]
    
    n, m = 20, 20
    neh_perm = [15, 14, 9, 7, 8, 11, 12, 10, 0, 19, 13, 16, 1, 17, 4, 5, 6, 18, 2, 3]
    
    # n, m = 200, 10
    # neh_perm = [158, 171, 15, 68, 197, 149, 161, 163, 103, 65, 133, 185, 122, 164, 82, 119, 13, 63, 74, 41, 192, 199, 7, 52, 62, 116, 1, 174, 106, 198, 134, 193, 131, 24, 17, 18, 37, 101, 23, 188, 8, 178, 153, 34, 173, 25, 81, 91, 114, 191, 96, 195, 12, 16, 39, 73, 107, 19, 130, 88, 170, 43, 180, 120, 104, 115, 186, 152, 117, 78, 184, 165, 57, 10, 143, 47, 127, 118, 176, 31, 61, 4, 53, 121, 55, 111, 85, 6, 105, 137, 69, 30, 9, 11, 142, 144, 100, 87, 3, 140, 71, 125, 45, 113, 183, 58, 138, 94, 67, 83, 54, 21, 20, 40, 79, 50, 110, 26, 49, 129, 22, 72, 151, 132, 64, 86, 93, 154, 128, 0, 126, 70, 14, 60, 97, 56, 109, 194, 155, 166, 167, 175, 189, 29, 35, 75, 2, 190, 76, 159, 84, 169, 80, 124, 123, 141, 139, 42, 172, 38, 27, 36, 168, 160, 108, 182, 162, 48, 90, 177, 187, 145, 196, 95, 5, 59, 51, 147, 66, 99, 181, 112, 89, 146, 157, 136, 32, 46, 156, 28, 150, 92, 102, 33, 148, 44, 179, 135, 77, 98]

    operation_times = read_operations(n, m)
    failure_size = 0.1
    fs_rmb = FlowShopWithMachineBreakdown(m, n, operation_times, failure_size)
    # fs_rmb.plot_sample()


    
    # import itertools
    # # all_perms = list(itertools.permutations(list(i for i in range(n))))
    # all_perms = []
    # optim_perm = [3, 17,	15,	8,	9,	6,	5,	14,	16,	7,	11,	13,	18,	19,	1,	4,	2,	10,	20,	12]
    # optim_perm_idxs = [x-1 for x in optim_perm]
    # all_perms.append(optim_perm_idxs)
    best_makespan = float("inf")
    best_permutation = []
    best_schedule = []
    makespan_list = []
    
    all_perms = []
    all_perms.append(neh_perm)

    for permutation in all_perms:
        makespan = fs_rmb.calculate_makespan(permutation)
        schedule = fs_rmb.get_schedule()

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
