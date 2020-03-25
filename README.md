# COVID-ClusteredSimulation
SImulation of dissease spreading with clustered connections

Proposed simulation extends standard SIR model, adding typical reasons for population mobility and movement. 
Simulation granularity is therefore extended and the modeling on the level of connections inside and inter city is implemented.
The small dense clusters representing families and larger representing working spaces are present and can be described by an 
integer parameter. It is possible to observe the impact of closing small larger bussineses or completely blocking random 
connections. The modularity of the code allows adding of new connection types and seeing the results.

People are represented by the vector containing integer number for every person living in the country. Value greater than zero means the individual is infected, the value itself represent the time until recovery. Contact between people is modeled by a sparse matrix containing every possible connection fo two individuals in the country. The diagonal represents the contact of a person with himself. Matrix elements close to the diagonal represent the people near where an individual lives. 

## Processes considered in the matrix creation:

* Family matrix: Depending on the typical distribution of household size, small clusters are created as diagonal blocks in the matix representing instant infection within family once one of its members is infected. The distribution of households represent the [data from the US](https://www.statista.com/statistics/242189/disitribution-of-households-in-the-us-by-household-size/), since we could not find data for CZ after a brief search. This matrix usually contains a lot of connections and is constant over time. 
* Companies and their office spaces: Represented by the square cluster of size n*n where n is the company size. The size of the company is obtained by samling the gamma distribution, the closest fit of the data from [this paper](http://aei.pitt.edu/36434/). This matrix can be constant in time, or can change if the scenario of the simulation calculates with the closing or reopening of office spaces.
* Connections inside the city: Random connections within one city where one has a probability CC that he meets a person and creates a potentialy infectious connection.
* Connections inside the country: Random connections over the entire country where one has a probability RC that he meets a person and creates a potentialy infectious connection.

These matrices are individually generated and summed together to create a global matrix of infectious connections withing a country. Dynamics of infection is then governed by the standard SIR model, however, the vectors have  the size of entire population. S and R are only the vectors of boolean value (although represented by the integer in the code) and I handled as described above. 

### Model parameters

Tht model contains three basic fittable parameters and others that can be inferred from existing data. The parameters that need to be fitted from the existing data about the infection are

* The amount of random infectious connection within a city. These are connected for example by public transport, shopping or work related meetings. The coeficient CC (city connections) is to be determined from known infectivity of the dissease since we do not know the probability of transmission between two individuals.
* The amount of random infectious connections across the whole country. Coeficient RC (random connections)
* Number of connection inside the company. (FC firm connections) How many people can you come into contact with at the office. 

### The parameters we can estimate with already existing data are

* Number of companies with no home office recommendation.
* Distribution of the number of employees.
* Household size distribution.
 
When the random parameters CC and RC are set high the model behaves as the standard SIR model. When there are measuser in place, reducing the random contact of the population the mobility is no longer random and model shows slower increase in the number of infected even when the companies remain open. Since the people tent to be clustered, the connections are largely static and the dissease does not spread that fast. Just think about how many new people you meet these days. 
 
The results of simple simulations can be seen in the Medium article. The importance of reducing random connections is shown there. 
 
The model is by no means complete and the furher contributions are encouraged. It could use more precise data for example:

* Household distribution for the particular republic you are modeling
* The number of working firms and the number of their employees present at the workspace. This can be for example reported by the companies
* Any data about any cluster that exists but was not included. Schools (when they open), dorms, houses for the elderly

The code can also use further improvements for example:
* Scenario creation
* Speedup 

The hardest of the tasks is of course the RC and CC fitting. Data from the operators together with the infection spreading dynamics observed in other countries may help to create a very precise simulation.

