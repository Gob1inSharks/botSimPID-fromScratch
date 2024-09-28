import matplotlib.pyplot as plt
import numpy as np

from spring import MassSpringDamperSystem

TIME_START = 0
TIME_STOP = 60
TIME_INCREMENTS = 0.1

DAMPING_CONSTANT = 4
MASS = 20
FORCE = 5
SPRING_CONSTANT = 2

INITIAL_POSITION = 0
INITIAL_VELOCITY = 0

if __name__ == "__main__":

    plant = MassSpringDamperSystem(SPRING_CONSTANT, DAMPING_CONSTANT, MASS, FORCE)

    initial_conditions = (INITIAL_POSITION, INITIAL_VELOCITY)

    time_intervals = (TIME_START, TIME_STOP, TIME_INCREMENTS)

    time = plant.getTime(TIME_START, TIME_STOP, TIME_INCREMENTS)

    position = plant.getPosition(initial_conditions, time_intervals)

    velocity = plant.getVelocity(initial_conditions, time_intervals)

    plt.plot(time, position)
    plt.title('Displacement of a Mass-Spring-Damper System vs Time')
    plt.grid()
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (m)')
    plt.show()