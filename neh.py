""""""

from email.policy import strict
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

def neh_add_task(i, d, perm):
    for suggested_place in range(len(perm)+1):


def neh(d:t_operation_times, n:int, m:int) -> t_neh_result:
    # 1) posortuj zadania od najdluzszego
    # task durations - how much time each tasks spends in a factory
    td = column_sum(d)
    # td w/ idx - list of tuples such as: (task_duration, idx)
    td_w_idx = list(zip(td, range(len(td))))
    td_w_idx.sort(reverse=True)

    # 2) dorzucaj po kolei minimalizujac makespan
    final_permutation = []
    for makespan, idx in td_w_idx:
        neh_add_task(idx, d, final_permutation)

https://github.com/martinWANG2014/TP_Johnson_CDS_NEH/blob/master/neh.py
https://github.com/pieetrus/SPD/blob/master/neh-python/main.py

    print(f"{td_w_idx=}")

    return ([2, 2], 3)

def main():
    n, m = 4, 3
    operation_times = read_operations(n, m)
    
    permutation, makespan = neh(operation_times, n, m)
    print(f"{permutation = }")
    print(f"{makespan = }")




if __name__ == '__main__':
    main()
