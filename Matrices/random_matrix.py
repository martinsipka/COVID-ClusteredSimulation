import numpy as np
from scipy.sparse import csr_matrix, random

class RandomMatrix:
    def construct(c_pop, RC):
        tot_pop = c_pop.sum()
        xs = np.random.choice(tot_pop, size = int(RC*tot_pop), replace=False)
        ys = np.random.choice(tot_pop, size = int(RC*tot_pop), replace=False)
        return csr_matrix((np.ones(int(RC*tot_pop)), (xs, ys)), shape=(tot_pop, tot_pop))


    def get_matrix(c_pop, RC):
        return RandomMatrix.construct(c_pop, RC)

    def shuffle(matrix):
        index = np.arange(np.shape(matrix)[0])
        np.random.shuffle(index)
        return matrix[index, :]
