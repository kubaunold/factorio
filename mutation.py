import itertools
import numpy as np

def mutation(sol):

    pos = list(np.random.permutation(np.arange(len(sol)))[:2])
        
    if pos[0] > pos[1]:
        t = pos[0]
        pos[0] = pos[1]
        pos[1] = t
    
    remJob = sol[pos[1]]
    
    for i in range(pos[1], pos[0], -1):
        sol[i] = sol[i-1]
        
    sol[pos[0]] = remJob
    return sol
