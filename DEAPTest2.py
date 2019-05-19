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
import pickle
import random
from functools import reduce

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import APFEncoding
import PythonSimpleSimulationStartup


#CONSTANTS
NGEN = 20 # Number of generations
NPOP = 30 # Number of individuals
CXPB = 0.8 # Probability of crossover
MUTPB = 1.0 # Probability of mutation
INDPB = 1/APFEncoding.APFEncoding.numberOfBits # Probability of each bit flipping
FREQ = 1 # How often to save progress (1 = every generation)




def createToolbox():
    toolbox = base.Toolbox()
    
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

    # Attribute generator
    toolbox.register("attr_bool", random.randint, 0, 1)
    
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, APFEncoding.APFEncoding.numberOfBits)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Create Operators
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=1/APFEncoding.APFEncoding.numberOfBits)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return toolbox

def oldcreateStats():
    # Needed for compatibility reasons
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("Q1", lambda x: numpy.percentile(x,25))
    stats.register("Q3", lambda x: numpy.percentile(x,75))
    stats.register("meadian", lambda x: numpy.percentile(x,50))

def createStats():
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("Q1", lambda x: numpy.percentile(x,25))
    stats.register("Q3", lambda x: numpy.percentile(x,75))
    # Note was mispelled before Feb 27 (may mess with loading files with pickle)
    stats.register("median", lambda x: numpy.percentile(x,50))
    
    # Added Feb 27
    stats.register("min", lambda x: numpy.argmin(x))
    stats.register("max", lambda x: numpy.argmax(x))
    return stats

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

def main(checkpoint=None):
    
    toolbox = createToolbox()
    stats = createStats()
    
    if checkpoint:
        # A file name has been given, then load the data from the file
        with open(checkpoint, "rb") as cp_file:
            cp = pickle.load(cp_file)
        population = cp["population"]
        start_gen = cp["generation"]
        halloffame = cp["halloffame"]
        logbook = cp["logbook"]
        random.setstate(cp["rndstate"])
    else:
        # Start a new evolution
        population = toolbox.population(n=NPOP)
        start_gen = 0
        halloffame = tools.HallOfFame(maxsize=1)
        logbook = tools.Logbook()
    
    for gen in range(start_gen, NGEN):
        print(gen)
        population = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        halloffame.update(population)
        record = stats.compile(population)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)

        population = toolbox.select(population, k=len(population))

        if gen % FREQ == 0:
            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cp = dict(population=population, generation=gen, halloffame=halloffame,
                      logbook=logbook, rndstate=random.getstate())

            with open("Mar31Full_run.pkl", "wb") as cp_file:
                pickle.dump(cp, cp_file)
                
    return population, logbook, record
        

#def main():
#    random.seed(74)
#    
#    pop = toolbox.population(n=50)
#    hof = tools.HallOfFame(1)
#    stats = tools.Statistics(lambda ind: ind.fitness.values)
#    stats.register("avg", numpy.mean)
#    stats.register("std", numpy.std)
#    stats.register("min", numpy.min)
#    stats.register("max", numpy.max)
#    
#    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.80, mutpb=1.0, ngen=40, 
#                                   stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof

if __name__ == "__main__":
    #pop, log, hof = main("checkpoint_name.pkl")
    pop, log, hof = main("Mar31Full_run.pkl")
    print(pop)
    print(log)
    print(hof)