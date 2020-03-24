import pickle
import random
import numpy as np
from scipy.sparse import csr_matrix, diags

largest_fam = 5
#                        (1    2     3     4     5) avg = 2.32
household_distribution = [0.3, 0.35, 0.15, 0.13, 0.07]


class FamilyMatrix:
    def set_diags(pos, size, diags):
        for i in range(0,largest_fam):
            upper_index = max(0, size-i-1)
            diags[i][pos:pos+upper_index] = 1

    def construct(c_pop):
        tot_pop = c_pop.sum()
        off_diags = [np.zeros(tot_pop-j) for j in range(1,largest_fam+1)]
        picked = 0
        offset = 0
        for i in range(0, len(c_pop)):
            print("Generating families for city ", i)
            while True:
                fam_size = np.random.choice(range(1,largest_fam+1), p = household_distribution)
                FamilyMatrix.set_diags(picked, fam_size, off_diags)
                picked += fam_size
                if(picked - offset > c_pop[i] - largest_fam):
                    FamilyMatrix.set_diags(picked, c_pop[i] + offset - picked, off_diags)
                    picked = offset + c_pop[i]
                    offset = picked
                    break

        country_matrix = diags(off_diags, list(range(1,largest_fam+1)))
        country_matrix += country_matrix.transpose()

        with open("Matrices/family_matrix.mtx", "wb") as output_file:
            pickle.dump(country_matrix, output_file)

        return country_matrix

    def get_matrix(c_pop):
        try:
            with open("Matrices/family_matrix.mtx", "rb") as output_file:
                mtx = pickle.load(output_file)
                if mtx.shape[0] == c_pop.sum():
                    return mtx
                else:
                    return FamilyMatrix.construct(c_pop)
        except IOError:
            return FamilyMatrix.construct(c_pop)
