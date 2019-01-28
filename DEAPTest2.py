#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
from functools import reduce

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import APFEncoding
import PythonSimpleSimulationStartup

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, APFEncoding.APFEncoding.numberOfBits)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    #convert bitArray to bitString
    bitString = reduce(lambda x, y: str(x) + str(y), individual)
    
    obj = APFEncoding.APFEncoding.APFEncodingFromBitString(bitString)
    print("{} {} {}".format(bitString, obj, obj.isValid()), end='')
    if(not obj.isValid()):
        return float("inf"),
    else:
        #print("Starting Simulation")
        fitness = PythonSimpleSimulationStartup.startSimulation(obj)
        #print("Simulation finished! Fitness: {}".format(fitness))
        print(" {}".format(fitness))
        if(fitness == 0.0):
            return float("inf"),
        return fitness,

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(74)
    
    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
                                   stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof

if __name__ == "__main__":
    pop, log, hof = main()
    print(pop)
    print(log)
    print(hof)