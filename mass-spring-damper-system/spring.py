from scipy.integrate import odeint as integrate
import numpy as np

class MassSpringDamperSystem:

    def __init__(self, springConstant, dampingConstant, mass, force):

        self.k = springConstant
        self.c = dampingConstant
        self.m = mass

        self.f = force

    def model(self, x, t):

        dydt = [0,0]

        dydt[0] = x[1] 
        dydt[1] = (self.f - self.k * x[0] - self.c * x[1]) / self.m

        # see readme for more details
        return dydt
    
    def getTime(self, start, stop, increments):

        return np.arange(start, stop, increments)
    
    def getModelResults(self,initial_conditions, time_intervals):

        #initial_conditions = (0, 0) this should be a tuple
        #time_intervals = (start, stop, increments) this should be a tuple

        tStart = time_intervals[0]
        tStop = time_intervals[1]
        tIncrements = time_intervals[2]

        t = self.getTime(tStart, tStop, tIncrements)

        # see readme for more
        return integrate(self.model, initial_conditions, t) #this uses odeint
    
    def getPosition(self, intial_conditions, time_intervals):

        results = self.getModelResults(intial_conditions, time_intervals)

        return results[:,0]
    
    def getVelocity(self, intial_conditions, time_intervals):

        results = self.getModelResults(intial_conditions, time_intervals)

        return results[:,1]

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    TIME_START = 0
    TIME_STOP = 60
    TIME_INCREMENTS = 0.1

    DAMPING_CONSTANT = 4
    MASS = 20
    FORCE = 5
    SPRING_CONSTANT = 2

    INITIAL_POSITION = 0
    INITIAL_VELOCITY = 0

    plant = MassSpringDamperSystem(SPRING_CONSTANT, DAMPING_CONSTANT, MASS, FORCE)

    initial_conditions = (INITIAL_POSITION, INITIAL_VELOCITY)

    time_intervals = (TIME_START, TIME_STOP, TIME_INCREMENTS)

    time = plant.getTime(TIME_START, TIME_STOP, TIME_INCREMENTS)

    position = plant.getPosition(initial_conditions, time_intervals)

    #velocity = plant.getVelocity(initial_conditions, time_intervals)

    plt.plot(time, position)
    plt.show()