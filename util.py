def read_operations(m, n):
    durations = []
    with open(f'test_data/operations_{m}_{n}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            machine_operations = map(int, line.split())
            durations.append(list(machine_operations))
    return durations

# print(read_operations(3, 4))


def silnia(n): return n*silnia(n-1) if n > 1 else 1


def average_of_list(m: list[list[int]]) -> list[int]:
    """From 2D list creates 1D list, where cell is an average value of whole column"""
        
    avg_list = [0] * len(m[0])

    # calculate sum
    for c in range(len(m[0])):
        # for each column
        for r in range(len(m)):
            # for each row
            avg_list[c] += m[r][c]
    
    # calculate average
    avg_list = [x/len(m) for x in avg_list]

    return avg_list

def who_is_the_best(perm_and_makespan_list):
    res = []
    
    #get last elements
    for i in perm_and_makespan_list:
        res.append(i[-1])

    def my_func(x):
        p, m = x
        return m

    res.sort(key = my_func) # smallest makespan value at the beginning
    return res[0]

if __name__ == '__main__':
    m = [[1,2,3,4, 7], [5,6,7,8, 11]]
    print(average_of_list(m))