#!/usr/bin/env python
import numpy as np
import sys
import os
import pandas as pd
import random
import numpy as np
import pandas as pd
import pickle
import argparse
import plotly.graph_objects as go
import matplotlib.pyplot as plt


sys.path.append(os.path.abspath("./Matrices"))
from family_matrix import FamilyMatrix
from city_matrix import CityMatrix
from work_matrix import WorkMatrix
from random_matrix import RandomMatrix

parser = argparse.ArgumentParser()
parser.add_argument("--CC", default=0.02, type=float, help="City connections parameter")
parser.add_argument("--RC", default=0.02, type=float, help="Random connections parameter")
parser.add_argument("--FC", default=5, type=int, help="Firm connections")
parser.add_argument("--NC", default=5000, type=int, help="Number of companies")
parser.add_argument("--steps", default="200", type=int, help="Simulation steps")
parser.add_argument("--start_infected", default=300, help="Infected at the beginning")
parser.add_argument("--prefix", default = "", help="Output files prefix.")
args = parser.parse_args([] if "__file__" not in globals() else None)

#PARAMETERS
#City coeficient
CC = args.CC
#Random coeficient
RC = args.RC
#Number of companies
NC = args.NC
#Connections inside firm
FC = args.FC
#Simulation steps
nSteps = args.steps
start_infected = args.start_infected
#Name prefix
prefix = args.prefix


cities = pd.read_csv('CZData/ludia.csv', sep=";")
c_pop = np.array(cities['pop'])
tot_pop = c_pop.sum()


print("Loading family matrix")
family_mtx = FamilyMatrix.get_matrix(c_pop)
print("Loading city matrix")
city_mtx = CityMatrix.get_matrix(c_pop, CC)
print("Loading work matrix")
work_mtx = WorkMatrix.get_matrix(c_pop, NC)
print("Loading random matrix")
random_mtx = RandomMatrix.get_matrix(c_pop, RC)

print("Family connections: " + str(family_mtx.nnz))
print("City connections: " + str(city_mtx.nnz))
print("Work connections: " + str(work_mtx.nnz))
print("Random connections: " + str(random_mtx.nnz))


constant_mtx = family_mtx + work_mtx
final_mtx = constant_mtx + random_mtx + city_mtx
print("Connections: ", final_mtx.nnz)
print("Simulation")

susc = np.full([tot_pop], 1)
infected = np.zeros(tot_pop)
recovered = np.zeros(tot_pop)

#Initialize infected
elements = random.sample(range(0, tot_pop), start_infected)
for e in elements:
    infected[e] = 14

#SIMULATION
infected_total = [start_infected]
daily = [0]
recovered_total = [0]
for i in range(1, nSteps+1):
    print("run no.", i)

    #Find recovered
    infected -= infected > 0
    recovered += infected == 1

    #Get new potentially infected
    potentially_infected = constant_mtx.dot(infected) + random_mtx.dot(infected) + city_mtx.dot(infected)

    #New infections - delete non-susceptible
    new_infect = np.logical_and(susc, potentially_infected)
    #Updaete susceptible status
    susc -= new_infect

    #Add new infections
    infected += 14*new_infect

    total = (infected > 0).sum()
    newInf = (new_infect > 0).sum()
    recTot = (recovered > 0).sum()
    print("Total: ", total)
    infected_total.append(total)
    print("New: ", newInf)
    daily.append(newInf)
    print("Recovered total", recTot)
    recovered_total.append(recTot)

    if total == 0:
        break

    #Rerandomize matrices
    print("Loading city matrix")
    city_mtx = CityMatrix.get_matrix(c_pop, CC)
    print("Loading random matrix")
    random_mtx = RandomMatrix.get_matrix(c_pop, RC)

name = prefix + "CC" + str(CC) + "RC" + str(RC) + "NC" + str(NC)

fig = plt.figure()
ax = plt.subplot(1, 3, 1)
plt.plot(infected_total)
plt.title('Total number of infected', fontsize=20)
plt.xlabel('Day', fontsize=18)
plt.ylabel('N. of people', fontsize=18)
#fig.savefig("figures/total" + name + ".jpg")

plt.subplot(1, 3, 2, sharey=ax)
plt.plot(daily)
plt.title('Daily new cases', fontsize=20)
plt.xlabel('Day', fontsize=18)
#fig.savefig("figures/daily" + name + ".jpg")

plt.subplot(1, 3, 3, sharey=ax)
plt.plot(recovered_total)
plt.title('Total recovered', fontsize=20)
plt.xlabel('Day', fontsize=18)
fig.savefig("figures/total" + name + ".jpg")

with open("results/"+name+"txt", 'w') as f:
    for tot, day, rec in zip(infected_total, daily, recovered_total):
        f.write(str(tot) + '\t' + str(day) + '\t' + str(rec) + '\n')

plt.show()
