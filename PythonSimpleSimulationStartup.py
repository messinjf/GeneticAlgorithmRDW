import os

""" A very simple demonstrating for starting the RDW simulation from python, waiting for process to finish,
and then starting a new process. """

if __name__ == "__main__":
    path = "C:\\Users\\messinjf\\Documents\\RDWSimulationStandalone"
    processName = "RDWSimulation.exe"
    #os.system(path + os.sep + processName)
	
    #parameters
    wallScalingFactor = 0.01
    wallFalloffFactor = 2.4
    userFalloffFactor = 3.0
    userHeuristic = "average"
    wallHeuristic = "normal"
	
    for i in range(1,10):
        arguments = " {} {} {} {} {}".format(i * wallScalingFactor, wallFalloffFactor, userFalloffFactor, userHeuristic, wallHeuristic)
        fitness = os.system(path + os.sep + processName + arguments)
        fitness = float(fitness) / (10.0 ** 6.0)
        print(fitness)