import pickle
import random
import numpy as np
from scipy.sparse import csr_matrix


gamma_shape = 2
avg_employees = 40
contacts_inside = 5

class WorkMatrix:
    def construct(c_pop, n_companies):
        tot_pop = c_pop.sum()
        xs = []
        ys = []
        for i in range(0, n_companies):
            #choose distribution for the cluster size
            size = int(np.random.gamma(gamma_shape, avg_employees/gamma_shape))
            x_position = random.randint(0, tot_pop - size)
            y_position = int(np.random.normal(x_position, 10000))
            y_position = max(0, min(y_position, tot_pop - 1 - size))
            xs += random.choices(range(x_position, x_position + size), k=min(size, contacts_inside))
            ys += random.choices(range(y_position, y_position + size), k=min(size, contacts_inside))

        work_mtx = csr_matrix((np.ones(len(xs)), (xs, ys)), shape=(tot_pop, tot_pop))

        with open("Matrices/work_matrix.mtx", "wb") as output_file:
            pickle.dump(work_mtx, output_file)

        return work_mtx


    def get_matrix(c_pop, n_companies):
        return WorkMatrix.construct(c_pop, n_companies)
