import random
import numpy as np

random.seed(10)

class VexBot:

    def __init__(self):

        self.P  = 0.3
    
        self.position = [0,0] #

        self.speed = 0
        self.MAX_SPEED = 2

        self.direction = 0 #in degree
        self.DIRECTION_NOISE_MAGNITUDE = 0.01 #also in degree

        self.gyro = 0

        self.motor = [10,10] #six motor drive train, so we can simplify it to one motor on each side
        # this can be seem as the acclearation we give to the bot
        # reality, the input is a voltage, which creates a force on the bot

    def noise(self):

        self.direction = self.direction + float((random.randint(int(-self.DIRECTION_NOISE_MAGNITUDE*1000), int(self.DIRECTION_NOISE_MAGNITUDE*1000))))/1000 #random.randint(-10,10)        

    def updateSpeed(self,dt):

        if self.speed < self.MAX_SPEED:
            self.speed += ((self.motor[0]+self.motor[1])/2)*dt
        else:
            self.speed = self.MAX_SPEED
            
    def updateDirection(self,dt):

        self.noise() #add some natural noise

        self.direction += (self.motor[0]-self.motor[1])*self.P

        if self.direction > 360:    
            self.direction = self.direction - 360

    def updateGyro(self):

        self.gyro = self.direction


    def update(self,dt):

        self.updateDirection(dt)

        self.updateSpeed(dt)

        self.updateGyro()

        self.position[0] += np.cos(np.deg2rad(self.direction)) * self.speed
        self.position[1] += np.sin(np.deg2rad(self.direction)) * self.speed

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    import utils

    TIME_START = 0
    TIME_STOP = 60
    TIME_INCREMENTS = 0.1

    INITIAL_POSITION = 0
    INITIAL_VELOCITY = 0

    bot = VexBot()

    initial_conditions = (INITIAL_POSITION, INITIAL_VELOCITY)

    time = utils.getTime(TIME_START, TIME_STOP, TIME_INCREMENTS)

    position_y = []

    for dt in time:

        bot.update(dt)

        position_y.append(bot.position[1])

        print(dt,bot.position[1],bot.gyro)

    #print(time) #for debugging
    #print(position)

    plt.plot(time, position_y)

    plt.show()