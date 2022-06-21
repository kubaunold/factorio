"""
https://github.com/martinWANG2014/TP_Johnson_CDS_NEH/blob/master/neh.py
https://github.com/pieetrus/SPD/blob/master/neh-python/main.py

"""

from util import read_operations

"""
DZIAŁANIE NEH'a
1) posortuj zadania od spędzającego najwięcej czasu w fabryce
2) popuj listę od początku

"""

# comment


t_permutation = list[int]
t_neh_result = t_permutation, int
t_operation_times = list[list[int]]



def column_sum(d:t_operation_times) -> list[int]:
    """calculates sum of rows in a matrix. Returns list"""
    # asterix in matrix transposes it
    # map applies sum function to each object on the right
    return list(map(sum, zip(*d)))

def technological_ancestor_finish(permutation, m, n,    op_times) -> int:
    """Calculates finish time of an operation, that's a technological predecessor
    to operation[m][n]"""
    if m == 0 and n == 0:
        return 0
    elif m == 1 and n == 0:
        return op_times[m-1][permutation[n]]
    elif m > 1 and n == 0:
        return technological_ancestor_finish(permutation, m-1, n, op_times)

    elif m == 0 and n == 

    elif m != 0 and n == 0:
        return start_times[m-1][permutation[n]] + op_times[m-1][permutation[n]]
    elif m == 0 and n != 0:
        return 0
    elif m != 0 and n != 0:
        return start_times[m-1][permutation[n]] + op_times[m-1][permutation[n]]

def machine_ancestor_finish(self, permutation, m, n,    op_times, start_times) -> int:
    """Calculates finish time of an operation, that's an order predecessor
    to operation[m][n]"""
    if m == 0 and n == 0:
        return 0
    elif m != 0 and n == 0:
        return 0
    elif m == 0 and n != 0:
        return start_times[m][permutation[n-1]] + op_times[m][permutation[n-1]]
    elif m != 0 and n != 0:
        return start_times[m][permutation[n-1]] + op_times[m][permutation[n-1]]



def calculate_makespan(permutation, op_times, num_tasks, num_machines) -> int:
    for m in range(num_machines):
        for n in range(num_tasks):
            # technological ancestor finish - finish time of an operation that's a tech predecessor
            # poprzednik technologiczny - operacja z tego zadania, ale poprzedniej maszyny
            taf = technological_ancestor_finish(permutation, m, n,  op_times)
            # machine ancestor finish - finish time of an operation that's an oredr predecessor
            # poprzednik kolejnościowy - inne zadanie z tej samej maszyny
            maf = machine_ancestor_finish(permutation, m, n,  op_times)
            
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



# def calculate_makespan(perm, d):
#     return 5

def neh_add_task(i:int, d:t_operation_times, perm:t_permutation) -> t_permutation:
    """ Adds task to final permutation 
        i - tasks' index
        d - operation times
        perm - final permutation """


    best_makespan = float("inf")
    best_idx_to_insert = None

    for idx in range(len(perm) + 1):
        # check all possible places (indexes from 0..len(perm))
        perm.insert(idx, i)
        temp_makespan = calculate_makespan(perm, d, n=len(perm), m=len(d))

        if(temp_makespan < best_makespan):
            # check if found better place
            best_makespan = temp_makespan
            best_idx_to_insert = idx
        
        _ = perm.pop(idx) #pop from list after check is done

    # Insert at best possible place
    perm.insert(best_idx_to_insert, i)
    return perm



            
            
            


def neh(d:t_operation_times, n:int, m:int) -> t_neh_result:
    # 1) posortuj zadania od najdluzszego
    # task durations - how much time each tasks spends in a factory
    td = column_sum(d)
    # td w/ idx - list of tuples such as: (task_duration, idx)
    td_w_idx = list(zip(td, range(len(td))))
    td_w_idx.sort(reverse=True)

    # 2) dorzucaj po kolei minimalizujac makespan
    final_permutation = []
    for task_duration, task_idx in td_w_idx:
        # Add tasks one by one
        final_permutation = neh_add_task(task_idx, d, final_permutation)


    print(f"{td_w_idx=}")

    return (final_permutation, calculate_makespan(final_permutation, d))

def main():
    n, m = 4, 3
    operation_times = read_operations(n, m)
    
    permutation, makespan = neh(operation_times, n, m)
    print(f"{permutation = }")
    print(f"{makespan = }")




if __name__ == '__main__':
    main()
