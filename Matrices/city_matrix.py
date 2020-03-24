import random
import numpy as np
from scipy.sparse import csr_matrix

class CityMatrix:
    def construct(c_pop, CC):
        tot_pop = c_pop.sum()
        offset = 0
        xs = []
        ys = []
        for i in range(0, len(c_pop)):
            xs += random.sample(range(offset, offset + c_pop[i]), int(CC*c_pop[i]))
            ys += random.sample(range(offset, offset + c_pop[i]), int(CC*c_pop[i]))
            offset += c_pop[i]
        return csr_matrix((np.ones(len(xs)), (xs, ys)), shape=(tot_pop, tot_pop))

    def get_matrix(c_pop, CC):
        return CityMatrix.construct(c_pop, CC)
