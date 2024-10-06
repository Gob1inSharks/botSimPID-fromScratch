import random
import numpy as np
import cv2


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

    def updateMotors(self):

        if self.motor[0] > 10:
            self.motor[0] = 10
        elif self.motor[0] < -10:
            self.motor[0] = -10

        if self.motor[1] > 10:
            self.motor[1] = 10
        elif self.motor[1] < -10:
            self.motor[1] = -10


    def update(self,dt):

        self.updateDirection(dt)

        self.updateSpeed(dt)

        self.updateGyro()

        self.position[0] += np.cos(np.deg2rad(self.direction)) * self.speed
        self.position[1] += np.sin(np.deg2rad(self.direction)) * self.speed








class Car:

    def __init__(self,controller = None):

        self.MAX_SPEED = 4.5

        self.theta = 0

        self.NOISE_MAGNITUDE = 1
        
        self.s = [0,0]
        self.v = [0,0]
        self.V = [12,12]

        self.radius = 2.75 * 2.56

        self.TICK = 0.1 #dt

        self.controller = controller

        self.MAX_VOLTAGE = 12

        self.MAX_RPM = 400

        self.image = np.zeros((2000,1500,3), np.uint8)
        self.image[:, :, 0] = 255
        self.image[:, :, 1] = 255
        self.image[:, :, 2] = 255

    def setMotorsTo(self,V1,V2):

        if V1 > self.MAX_VOLTAGE:
            V1 = self.MAX_VOLTAGE
        elif V1 < 0:
            V1 = 0

        if V2 > self.MAX_VOLTAGE:
            V2 = self.MAX_VOLTAGE
        elif V2 < 0:
            V2 = 0

        self.V = [V1,V2]
        
    def vol2speed(self,V):

        rpm = 34 * V

        if rpm > self.MAX_RPM:
            rpm = self.MAX_RPM
        elif rpm < 0:
            rpm = 0

        return (2*np.pi*self.radius) * rpm / 60

    def run(self,totalTime):

        times = np.arange(0, totalTime, self.TICK)

        positions = [[],[]]

        for t in times:

            self.advance(1)

            positions[0].append(self.s[0])
            positions[1].append(self.s[1])

            cv2.waitKey(60)
            self.draw()
            cv2.imshow("image", self.image)

        #print(positions)

    def draw(self):

        cv2.drawContours(self.image, [self.s[0],self.s[1]], -1, (0,255,0), 3)

    def advance(self,ticks,dt = 0.1):

        for t in range(0,ticks): 

            self.v[0] = self.vol2speed(self.V[0])
            self.v[1] = self.vol2speed(self.V[1])

            if self.v[0] > self.MAX_SPEED:
                self.v[0] = self.MAX_SPEED
            elif self.v[0] < -self.MAX_SPEED:
                self.v[0] = -self.MAX_SPEED

            if self.v[1] > self.MAX_SPEED:
                self.v[1] = self.MAX_SPEED
            elif self.v[1] < -self.MAX_SPEED:
                self.v[1] = -self.MAX_SPEED

            self.v[0] -= random.randint(0, int(self.NOISE_MAGNITUDE*1000))/1000
            #self.v[1] -= random.randint(0, int(self.NOISE_MAGNITUDE*1000))/1000

            self.s[0] += self.v[0]*dt
            self.s[1] += self.v[1]*dt

            #print(self.v[0],self.v[1]) #for debugging
            print(self.s[0],self.s[1])
            

            



if __name__ == "__main__":

    vex = Car()
    vex.run(60)

    """

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
    """