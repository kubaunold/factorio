""""""

from pymysql import OperationalError
from util import read_operations

"""
DZIAŁANIE NEH'a
1) posortuj zadania od spędzającego najwięcej czasu w fabryce
2) popuj listę od początku

"""

Permutation = list[int]
NEH_result = Permutation, int
Operation_times = list[list[int]]


def neh(d:Operation_times, n:int, m:int) -> NEH_result:


    return ([2, 2], 3)

def main():
    n, m = 20, 5
    operation_times = read_operations(n, m)
    
    permutation, makespan = neh(operation_times, n, m)
    print(f"{permutation = }")
    print(f"{makespan = }")




if __name__ == '__main__':
    main()
