import itertools
import numpy as np
from base_logger import logger

def ordered_crossover(p1, p2) -> list:
    """ Ordered crossover 
        Link: https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35"""

    gene_A = int(np.random.random() * len(p1) + 0.5)
    gene_B = int(np.random.random() * len(p2) + 0.5)

    start_gene = min(gene_A, gene_B)
    end_gene = max(gene_A, gene_B)


    child_part1 = []
    child_part2 = []
    # assembly first part of a child (from parent1)
    for i in range(start_gene, end_gene):
        child_part1.append(p1[i])

    # assembly remaining part of a child (from parent2)
    child_part2 = [item for item in p2 if item not in child_part1]

    child = child_part1 + child_part2


    return child

# def two_point_crossover(one, two) -> list:
#     """ Two-point crossover """
#     if len(one) != len(two):
#         logging.critical("Crossover cannot take place. Parents have different size!")

#     pos = list(np.random.permutation(np.arange(len(one)-1)+1)[:2])
    
#     if pos[0] > pos[1]:
#         t = pos[0]
#         pos[0] = pos[1]
#         pos[1] = t
    
#     child = list(parents[0])
    
#     for i in range(pos[0], pos[1]):
#         child[i] = -1
    
#     p = -1
#     for i in range(pos[0], pos[1]):
#         while True:
#             p = p + 1
#             if parents[1][p] not in child:
#                 child[i] = parents[1][p]
#                 break
    
#     return child

if __name__=='__main__':
    p1 = [5, 4, 0, 3, 2, 1, 6]
    p2 = [2, 4, 1, 3, 6, 5, 0]

    print(ordered_crossover(p1, p2))
