# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:15:14 2019

@author: messinjf
"""

import array
import pickle
import random
from functools import reduce

import numpy
import matplotlib.pyplot as plt

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import APFEncoding
import PythonSimpleSimulationStartup

def getAttributeList(logbook, attribute):
    return [epoch[attribute] for epoch in logbook][:-1]

def main(checkpoint=None):
    # A file name has been given, then load the data from the file
    with open(checkpoint, "rb") as cp_file:
        cp = pickle.load(cp_file)
    population = cp["population"]
    start_gen = cp["generation"]
    halloffame = cp["halloffame"]
    logbook = cp["logbook"]
    
    print(population)
    print(start_gen)
    print(halloffame)
    print(logbook)
    
    best = halloffame[0]
    bitString = reduce(lambda x, y: str(x) + str(y), best)
    
    obj = APFEncoding.APFEncoding.APFEncodingFromBitString(bitString)
    print("{} {} {}".format(bitString, obj, obj.isValid()), end='')
    print(getAttributeList(logbook,"Q1"))
    epochs = range(1,len(logbook))
    plt.figure(figsize=(9, 6))
    plt.plot(epochs, getAttributeList(logbook,"Q1"), label="Q1")
    plt.plot(epochs, getAttributeList(logbook,"median"), label="median")
    plt.plot(epochs, getAttributeList(logbook,"Q3"), label="Q3")
    plt.hlines(2.82,1,20,color='r', linestyle='--', label="Random Search")
    plt.xticks(epochs)
    #plt.axis((0,20,0,4.5))
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Total Resets)')
    plt.title('Improvement of Fitness Over Time')
    plt.legend()
    #plt.show()
    plt.savefig("C:\\Users\\messinjf\\Desktop\\Results April 8th\\GAResults.png")
    
if __name__ == "__main__":
    #main("Feb18_2_1Rect.pkl")
    #main(".\Results\Feb18_2_1Rect_3_user.pkl")
    #main(".\Results\Feb21_L_shape_3user.pkl")
    #main(".\Results\Feb22_square40x40_7user.pkl")
    #main(".\Results\Feb23_square25x25_2user.pkl")
    #main(".\Results\Feb24_square30x30_3user.pkl")
    #main(".\Results\Feb16.pkl")
    #main(".\Results\Feb25_square30x30_3user_Cequals1.pkl")
    #main(".\Results\Feb26_square30x30_3user_Cequals1.pkl")
    #main(".\Results\Feb28Full_run.pkl")
    main(".\Results\Mar31Full_run.pkl")
    