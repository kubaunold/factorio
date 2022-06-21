import random
import numpy as np
from breakdown import Breakdown
from util import read_operations, sum_of_list

def generate_breakdown(op_times, n, m, failure_size):
    """ Generates breakdown based on failure_size param """
    makespan = sum_of_list(op_times[0])
    random.seed(10)     # TEMPORAL: unrandomize things
    breakdown_duration = max(random.randint(5,15), int(makespan * failure_size))
    return Breakdown(random.randint(0,m - 1), random.randint(0, makespan), breakdown_duration)


def read(nb):
    tasks = []
    with open('data\\NEH' + str(nb) + '.dat') as f:
        n, m = f.readline().split()  # n - zadań, m - maszyn
        for i in f:
            if not i.isspace():  # zabezpieczenie przed linią złożoną z samych białych znaków
                tasks.append([int(x) for x in i.split()])
    return tasks, int(n), int(m)


def read_results(nb):
    with open('data\\NEH' + str(nb) + '.OUT') as f:
        return int(f.readline())


# j-zadanie k-maszyna
# n-zadania m-maszyny
def OLD_c_max(tasks, n, m, breakdown:Breakdown):
    c = np.zeros((n+1, m+1))
    for j in range(0, n+1):     # j jest po zadaniach
        for k in range(0, m+1): # k jest po maszynach
            
            start_time = max(c[j-1][k], c[j][k-1])
            if(k==breakdown.m):
                if (start_time + tasks[j][k]) <= breakdown.t0:
                    # op will finish before the breakdown start
                    c[j][k] = max(c[j-1][k], c[j][k-1]) + tasks[j-1][k-1]
                else:
                    # op has to start after
                    c[j][k] = max(start_time, breakdown.t0 + breakdown.breakdown_duration)
            else:
                # there is no breakdown on this machine
                c[j][k] = max(c[j-1][k], c[j][k-1]) + tasks[j-1][k-1]
            

    return c

def c_max(tasks, n, m, breakdown:Breakdown):
    c = np.zeros((n+1, m+1))
    for idx_n in range(1, n+1):     # przejdz się po zadaniach
        for idx_m in range (1, m+1):    # przejdź się po maszynach
            c[idx_n][idx_m] = max(c[idx_n-1][idx_m], c[idx_n][idx_m-1]) + tasks[idx_n-1][idx_m-1]
            if (idx_m-1) == breakdown.m:
                # zlapalem maszyne, ktora ma breakdowna
                if c[idx_n][idx_m] <= breakdown.t0:
                    #to zdaze sie wykonac przed breakdownem
                    pass
                else:
                    # nie zdaze sie wykonac!
                    c[idx_n][idx_m] = max(c[idx_n][idx_m], breakdown.t0 + breakdown.breakdown_duration + tasks[idx_n-1][idx_m-1])
    return c



# sortuje listę zadań zgodnie z niemalejącą sumą czasów wykonania zadania
# na wszystkich maszynach
def sorted_by_p(tasks, n, m):
    permutation = []
    result = []
    for i in range(n):
        permutation.append(i)
    temp = sorted(permutation, key=lambda x: sum_p(tasks, x, m), reverse=True)
    for i in temp:
        result.append(tasks[i])
    return result


# zwraca sumę czasów wykonania zadania n na m maszynach
def sum_p(tasks, n, m):
    result = 0
    for i in range(m):
        result += tasks[n][i]
    return result


# def get_permutation_from_sequence(sequence, tasks):
#     return None

# n - zadań
# m - maszyn
def neh(tasks, n, m, breakdown):
    tasks_lst = sorted_by_p(tasks, n, m)
    # current_task = tasks_lst[0]
    sequence = []
    best_sequence = []

    for t_idx in range(0, n): # dla każdego zadania
        print(t_idx)
        best_c_max = float("inf") # bardzo duża liczba

        for perm_pos in range(0, t_idx+1): # dla każdej pozycji w permutacji
            temp_sequence = list.copy(sequence)
            temp_sequence.insert(perm_pos, tasks_lst[t_idx])

            n = len(temp_sequence)
            c_max_seq = c_max(temp_sequence, n, m, breakdown)[n][m]
            if c_max_seq < best_c_max:
                best_sequence = temp_sequence
                best_c_max = c_max_seq

        sequence = best_sequence


    return int(best_c_max), sequence

def create_tasks(operation_times):
    arr1 = np.array(operation_times)
    arr1_transpose = arr1.transpose()
    return arr1_transpose.tolist()

if __name__ == '__main__':
    lst = []

    # n, m = 4, 3
    # n, m = 20, 5
    # n, m = 20, 20
    # n, m = 50, 10
    # n, m = 100, 20
    # n, m = 200, 10
    n, m = 500, 20
    operation_times = read_operations(n, m)
    tasks = create_tasks(operation_times)


    # Generate breakdown
    breakdown = generate_breakdown(operation_times, n, m, 0.10)

    neh_makespan, neh_sequence = neh(tasks, n, m, breakdown)


    neh_permutation = []
    for t in neh_sequence:
        neh_permutation.append(tasks.index(t))
    
    
    # check for the same tasks -> ERROR! :(
    if len(list(dict.fromkeys(neh_permutation))) != n:
        raise Exception("Sorry, there are multiple same tasks and i can calculate only for distinct tasks")


    str_res = f"{n=} {m=} {neh_makespan=} rmb_duration={breakdown.breakdown_duration} rmb_t0={breakdown.t0} rmb_m={breakdown.m} {neh_permutation=}"
    with open(f"results\\neh_results.txt", "a") as f:
            f.write(str_res + "\n")

    # for i in range(1, 10):
    #     tasks, n, m = read(i)

    #     print(str(i) + " - " + str(neh(tasks, n, m)) + " - " + str(read_results(i)))
