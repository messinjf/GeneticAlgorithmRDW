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
    
    paramDict = {"wallScalingFactor" : 20,
                  "wallFalloffFactor" : 13,
                  "userFalloffFactor" : 13,
                  "userForceHeuristic" : 2,
                  "wallForceHeuristic" : 1,
                  "distanceBetweenUsers" : 14,
                  "startingLineRotation" : 19}
    floatingPointParameters = ["wallScalingFactor", "wallFalloffFactor", "userFalloffFactor", "distanceBetweenUsers", "startingLineRotation"]
    integerParameters = ["userForceHeuristic", "wallForceHeuristic"]
    numberOfBits = reduce(lambda x, y: x + y, list(paramDict.values()))

    def __init__(self, wallScalingFactor = None, wallFalloffFactor = None,
                 userFalloffFactor = None, userForceHeuristic = None,
                 wallForceHeuristic = None, distanceBetweenUsers = None, startingLineRotation = None):
        #self.wallScalingFactor = wallScalingFactor
        #self.wallFalloffFactor = wallFalloffFactor
        #self.userFalloffFactor = userFalloffFactor
        #self.userForceHeuristic = userForceHeuristic
        #self.wallForceHeuristic = wallForceHeuristic
        self.dictionary = dict()
        self.parameters = (wallScalingFactor, wallFalloffFactor, userFalloffFactor,
                      userForceHeuristic, wallForceHeuristic, distanceBetweenUsers, startingLineRotation)
        for i, k in enumerate(APFEncoding.paramDict):
            self.dictionary[k] = self.parameters[i]        
    def __str__(self):
#        string = (str(self.wallScalingFactor) + " " +
#                  str(self.wallFalloffFactor) + " " +
#                  str(self.userFalloffFactor) + " " +
#                  str(self.userForceHeuristic) + " " +
#                  str(self.wallForceHeuristic))
        string = reduce(lambda x, y : str(x) + " " + str(y), self.parameters)
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
        
        bitStrEle = []
        bitStr = ""
        for i, k in enumerate(APFEncoding.paramDict):
            # Extract the part of the bitstring that corresponds to the current parameter
            if k in APFEncoding.floatingPointParameters:
                bitStr = f(self.dictionary[k], APFEncoding.paramDict[k], 1000)
            elif k in APFEncoding.integerParameters:
                bits = APFEncoding.paramDict[k]
                if k == "userForceHeuristic":
                    bitStr = f(APFEncoding.userForceHeuristicOptions.index(self.dictionary[k]),bits, 1)
                elif k == "wallForceHeuristic":
                    bitStr = f(APFEncoding.wallForceHeuristicOptions.index(self.dictionary[k]),bits, 1)
                else:
                    #Not yet implemented
                    assert(False)
            else:
                #Not yet implemented
                assert(False)
            bitStrEle.append(bitStr)
#        bitStrEle = (f(self.wallScalingFactor, 20, 1000) +
#                     f(self.wallFalloffFactor, 14, 1000) +
#                     f(self.userFalloffFactor, 14, 1000) +
#                     f(APFEncoding.userForceHeuristicOptions.index(self.userForceHeuristic), 2, 1) +
#                     f(APFEncoding.wallForceHeuristicOptions.index(self.wallForceHeuristic), 1, 1))
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
        dna = np.random.choice([0, 1], APFEncoding.numberOfBits)
        dna = reduce(lambda x, y: str(x) + str(y), dna)
        parameters = APFEncoding.decode(dna)
        obj = APFEncoding(*parameters)
        while(not obj.isValid()):
            dna = np.random.choice([0, 1], APFEncoding.numberOfBits)
            dna = reduce(lambda x, y: str(x) + str(y), dna)
            parameters = APFEncoding.decode(dna)
            obj = APFEncoding(*parameters)
        return obj
        
    @classmethod
    def APFEncodingFromBitString(cls, bitString):
        assert(len(bitString) == APFEncoding.numberOfBits)
        parameters = APFEncoding.decode(bitString)
        return APFEncoding(*parameters)
    
    """ Decode a bit string into a tuple of parameters. """
    @staticmethod
    def decode(bitString):
        
        # determine the start and endpoint of each parameter
        idxs = [reduce(lambda x, y: x + y, 
                       list(APFEncoding.paramDict.values())[:i+1])
                for i in range(len(APFEncoding.paramDict.values()))]
        idxs.insert(0,0)
        
        #list of floating point parameters
        parameters = []
        for i, k in enumerate(APFEncoding.paramDict):
            # Extract the part of the bitstring that corresponds to the current parameter
            parameter = bitString[idxs[i]:idxs[i+1]]
            if k in APFEncoding.floatingPointParameters:
                # convert from bit string to integer to float and divide by 1000
                value = int(parameter, 2)
                value = float(value) / 1000.0
                parameters.append(value)
            elif k in APFEncoding.integerParameters:
                # convert from bit string to integer
                value = int(parameter,2)
                if k == "userForceHeuristic":
                    value = APFEncoding.userForceHeuristicOptions[value]
                elif k == "wallForceHeuristic":
                    value = APFEncoding.wallForceHeuristicOptions[value]
                else:
                    #Not yet implemented
                    assert(False)
                parameters.append(value)
            else:
                #Not yet implemented
                assert(False)
        return tuple(parameters)
    
    def isValid(self):
        if self.parameters == None : return False
        return ((self.dictionary["wallScalingFactor"] > 0.0 and self.dictionary["wallScalingFactor"] < 1000.0) and
                (self.dictionary["wallFalloffFactor"] > 0.0 and self.dictionary["wallFalloffFactor"] < 10.0) and
                (self.dictionary["userFalloffFactor"] > 0.0 and self.dictionary["userFalloffFactor"] < 10.0) and
                (self.dictionary["distanceBetweenUsers"] > 2.0)
                )
    
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
        beforeStr = APFEncoding.getRandomBitString(APFEncoding.numberOfBits)
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