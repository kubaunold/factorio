def read_operations(m, n):
    durations = []
    with open(f'test_data/operations_{m}_{n}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            machine_operations = map(int, line.split())
            durations.append(list(machine_operations))
    return durations

# print(read_operations(3, 4))
