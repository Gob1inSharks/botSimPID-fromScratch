import matplotlib.pyplot as plt
import numpy as np
import random

from vexbot import VexBot
from botcontroller import Controller

import utils

TIME_START = 0
TIME_STOP = 60
TIME_INCREMENTS = 0.1

INITIAL_POSITION = 0
INITIAL_VELOCITY = 0

if __name__ == "__main__":

    bot = VexBot()

    control = Controller(bot)

    control.Kp = 2
    control.Kd = 0.012
    control.target = 0

    initial_conditions = (INITIAL_POSITION, INITIAL_VELOCITY)

    time = utils.getTime(TIME_START, TIME_STOP, TIME_INCREMENTS)

    position_y = []
    position_x = []

    for dt in time:

        bot.update(dt)

        control.updateMotors()

        position_y.append(bot.position[1])
        position_x.append(bot.position[0])

    #print(time) #for debugging
    #print(position)

    plt.plot(position_x, position_y)

    plt.show()