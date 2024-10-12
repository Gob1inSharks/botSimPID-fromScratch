import random
import numpy as np
import cv2
import pygame
import os
import sys

random.seed(10)

DIR = os.path.dirname(os.path.realpath(__file__))

BASE_IMAGE_PATH = '/assets/images' 
BASE_SETTINGS_PATH = '/assets/jsons'
DELETING_SUBDIRECTORIES = ['/__pycache__','/temp']
COLOUR_KEY = (0,0,0) #black

def load_image(path): 

    image = pygame.image.load(DIR+BASE_IMAGE_PATH+'/'+path).convert() #convert it for better performance Uwu It helps a lot 
    image.set_colorkey(COLOUR_KEY) #changes this colour into transparent 

    return image 

class VexCar:

    def __init__(self,controller = None):

        self.MAX_SPEED = 4.5

        self.theta = 0

        self.NOISE_MAGNITUDE = 1

        self.MASS = 10
        
        self.s = [0,0]
        self.v = [0,0]
        self.V = [12,12]

        self.RADIUS = 2.75 * 2.56

        self.TICK = 0.1 #dt
        self.FPS = 1/self.TICK

        self.controller = controller

        self.MAX_VOLTAGE = 12

        #pygame stuff

        pygame.init() 
        pygame.display.set_caption("VexCar Simulation") 

        self.SCENE_HIEGHT = 1080
        self.SCENE_WIDTH = 1920

        self.SCREEN_TO_SCENE_RATIO = 2

        self.SCENE_RATIO = float(self.SCENE_HIEGHT / self.SCENE_WIDTH)

        self.SCREEN_HEIGHT = self.SCENE_HIEGHT*self.SCREEN_TO_SCENE_RATIO
        self.SCREEN_WIDTH = self.SCENE_HIEGHT*self.SCREEN_TO_SCENE_RATIO

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.scene = pygame.Surface((self.DISPLAY_WIDTH,self.DISPLAY_HIEGHT))

        self.clock = pygame.time.Clock() 

        self.assets = { 
            "icon" : load_image("icon.png"), #todo create assets
        }

        self.timer = 0

    def set(self,V1,V2):

        if V1 > self.MAX_VOLTAGE:
            V1 = self.MAX_VOLTAGE
        elif V1 < 0:
            V1 = 0

        if V2 > self.MAX_VOLTAGE:
            V2 = self.MAX_VOLTAGE
        elif V2 < 0:
            V2 = 0

        self.V = [V1,V2]

    def states(self):

        return self.s,self.v,self.V

    def getSensor(self):

        return self.theta

    def setParameters(self,mass,radius,noise,tick):

        self.MASS = mass
        self.RADIUS = radius
        self.NOISE_MAGNITUDE = noise
        self.TICK = tick
        
    def vol2speed(self,V):

        rpm = 34 * V

        if rpm > self.MAX_RPM:
            rpm = self.MAX_RPM
        elif rpm < 0:
            rpm = 0

        return (2*np.pi*self.radius) * rpm / 60

    def run(self,totalSeconds):

        times = np.arange(0, totalSeconds, self.TICK)

        while True:

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 

            self.screen.fill((0,0,0)) 

            self.draw()

            pygame.display.update() 

            dt = self.clock.tick(self.FPS) * .001 * self.FPS

            self.timer += dt

            if self.timer > totalSeconds:
                pygame.quit() 
                sys.exit() 

            self.advance(dt = dt)

        #print(positions)

    def draw(self):

        cv2.drawContours(self.image, [self.s[0],self.s[1]], -1, (0,255,0), 3)

    def advance(self,dt = 0.1):

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

    vex = VexCar()
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