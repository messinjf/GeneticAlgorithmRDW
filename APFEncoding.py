# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 18:46:59 2019

@author: messinjf
"""

import numpy as np
from functools import reduce

class APFEncoding:
    
    userForceHeuristicOptions = ["none", "average", "max", "linear"]
    wallForceHeuristicOptions = ["normal", "pointing"]

    def __init__(self, wallScalingFactor = None, wallFalloffFactor = None,
                 userFalloffFactor = None, userForceHeuristic = None,
                 wallForceHeuristic = None):
        self.wallScalingFactor = wallScalingFactor
        self.wallFalloffFactor = wallFalloffFactor
        self.userFalloffFactor = userFalloffFactor
        self.userForceHeuristic = userForceHeuristic
        self.wallForceHeuristic = wallForceHeuristic
        
    def __str__(self):
        string = (str(self.wallScalingFactor) + " " +
                  str(self.wallFalloffFactor) + " " +
                  str(self.userFalloffFactor) + " " +
                  str(self.userForceHeuristic) + " " +
                  str(self.wallForceHeuristic))
        return string
    
    """ Encode the parameters as a string of 1s and 0s. """
    def encode(self):
        
        """ Function to convert each individual parameter given the number of
        bits to pad, and the factor to multiply the converted parameter by. """
        def f(x, bits, factor=1) :
            if(factor != 1):
                return str(bin(round(x * factor))).replace("0b", "").rjust(bits,"0")
            else:
                return str(bin(x)).replace("0b", "").rjust(bits,"0")
            
        
        bitStrEle = (f(self.wallScalingFactor, 20, 1000) +
                     f(self.wallFalloffFactor, 14, 1000) +
                     f(self.userFalloffFactor, 14, 1000) +
                     f(APFEncoding.userForceHeuristicOptions.index(self.userForceHeuristic), 2, 1) +
                     f(APFEncoding.wallForceHeuristicOptions.index(self.wallForceHeuristic), 1, 1))
        bitString = reduce(lambda x, y: x + y, bitStrEle)
        return bitString
                     
                     
    """ Create an APFEncoding with random values for each parameters. """
    @classmethod
    def random(cls):
        wallScalingFactor = np.round(np.random.random() * 1000, 3) + .001
        wallFalloffFactor = np.round(np.random.random() * 10, 3) + .001
        userFalloffFactor = np.round(np.random.random() * 10, 3) + .001
        userForceHeuristic = np.random.choice(APFEncoding.userForceHeuristicOptions)
        wallForceHeuristic = np.random.choice(APFEncoding.wallForceHeuristicOptions)
        return APFEncoding(wallScalingFactor, wallFalloffFactor,
                 userFalloffFactor, userForceHeuristic, wallForceHeuristic)
    
    
    """ Create an APFEncoding with random values by creating random bit
    strings and determining if they are valid. """
    @classmethod
    def randomBitString(cls):
        numberOfBits = 20 + 14 + 14 + 2 + 1
        
        parameters = None
        while(not APFEncoding.isValid(parameters)):
            dna = np.random.choice([0, 1], numberOfBits)
            dna = reduce(lambda x, y: str(x) + str(y), dna)
            parameters = APFEncoding.decode(dna)
        return APFEncoding(parameters[0], parameters[1],
                 parameters[2], parameters[3], parameters[4])
        
    @classmethod
    def APFEncodingFromBitString(cls, bitString):
        parameters = APFEncoding.decode(bitString)
        if(not APFEncoding.isValid(parameters)):
            pass
            #print("Warning: this bitString is not valid.")
        return APFEncoding(parameters[0], parameters[1],
                 parameters[2], parameters[3], parameters[4])
    
    """ Decode a bit string into a tuple of parameters. """
    @staticmethod
    def decode(bitString):
        
        a = 20
        b = a + 14
        c = b + 14
        d = c + 2
        e = d + 1
        
        #convert bitString to integer
        def f(x) : return int(x,2)
        #convert int to float and divide by 1000.0
        def g(x) : return float(x) / 1000.0
        
        wallScalingFactor = g(f(bitString[0:a]))
        wallFalloffFactor = g(f(bitString[a:b]))
        userFalloffFactor = g(f(bitString[b:c]))
        userForceHeuristic = APFEncoding.userForceHeuristicOptions[f(bitString[c:d])]
        wallForceHeuristic = APFEncoding.wallForceHeuristicOptions[f(bitString[d:e])]
        parameters = (wallScalingFactor, wallFalloffFactor, userFalloffFactor,
                      userForceHeuristic, wallForceHeuristic)
        
        #print("Input to decode: {}".format(bitString))
        #print("Resulting parameters: {}".format(parameters))
        return parameters
    
    @staticmethod
    def isValid(parameters):
        if parameters == None : return False
        return ((parameters[0] > 0.0 and parameters[0] < 1000.0) and
                (parameters[1] > 0.0 and parameters[1] < 10.0) and
                (parameters[2] > 0.0 and parameters[2] < 10.0))
    
    @staticmethod
    def getRandomBitString(bits):
        bitArray = np.random.choice([0, 1], bits)
        bitString = reduce(lambda x, y: str(x) + str(y), bitArray)
        return bitString

def unit_test_encode_decode():
    """Test 1: create random strings, decode, then encode and see assert that
    they are equal after the process.
    """
    for i in range(10**3):
        beforeStr = APFEncoding.getRandomBitString(20+14+14+2+1)
        obj = APFEncoding.APFEncodingFromBitString(beforeStr)
        afterStr = obj.encode()
        #obj2 = APFEncoding.APFEncodingFromBitString(afterStr)
        #print("Object: {}\n\tbefore: {}\n\tafter:  {}".format(obj, beforeStr, afterStr))
        #print("Object after: {}".format(obj2))
        assert(beforeStr == afterStr)

if __name__ == "__main__":
    #individual = APFEncoding.randomBitString()
    #print(individual)
    #print(individual.encode())
    unit_test_encode_decode()