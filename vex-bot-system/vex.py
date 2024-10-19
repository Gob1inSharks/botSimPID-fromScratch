import random
import numpy as np
import pygame
import os
import sys
import math

random.seed(10)

DIR = os.path.dirname(os.path.realpath(__file__))

BASE_IMAGE_PATH = '/assets/images' 
BASE_SETTINGS_PATH = '/assets/jsons'
DELETING_SUBDIRECTORIES = ['/__pycache__','/temp']
COLOUR_KEY = (0,0,0) #black

def load_image(path): 

    image = pygame.image.load(DIR+BASE_IMAGE_PATH+'/'+path).convert() 
    image.set_colorkey(COLOUR_KEY)

    return image 

class VexCar:

    def __init__(self,controller = None):

        self.MAX_SPEED = 200

        self.theta = 0

        self.NOISE_MAGNITUDE = 20

        self.MASS = 10
        
        self.s = [0,0]
        self.v = [0,0]
        self.V = [12,12]

        self.RADIUS = 2.75 * 2.56

        self.TICK = 0.1 #dt
        self.FPS = 10

        self.controller = controller

        self.MAX_VOLTAGE = 12

        #pygame stuff

        pygame.init() 
        pygame.display.set_caption("VexCar Simulation") 

        self.SCENE_HIEGHT = 1377
        self.SCENE_WIDTH = 1344

        self.SCREEN_TO_SCENE_RATIO = 1

        self.SCENE_RATIO = float(self.SCENE_HIEGHT / self.SCENE_WIDTH)

        self.SCREEN_HEIGHT = int(self.SCENE_HIEGHT*self.SCREEN_TO_SCENE_RATIO)
        self.SCREEN_WIDTH = int(self.SCENE_HIEGHT*self.SCREEN_TO_SCENE_RATIO)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.scene = pygame.Surface((self.SCENE_WIDTH,self.SCENE_HIEGHT))

        self.clock = pygame.time.Clock() 

        self.assets = {
            "field":load_image('field.png'),
        }

        self.timer = 0

        self.MAX_RPM = 400

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

        return (2*np.pi*self.RADIUS) * rpm / 60

    def run(self,totalSeconds):

        times = np.arange(0, totalSeconds, self.TICK)

        while True:

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 

            self.scene.fill((35,35,35)) 

            self.scene.blit(self.assets['field'],(0,0))

            self.draw(self.SCENE_WIDTH//2,self.s[0],100,100,(255,255,255))

            self.screen.blit(pygame.transform.scale(self.scene,(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)), (0,0)) 

            pygame.display.update() 

            dt = self.clock.tick(self.FPS) * .001 

            self.timer += dt

            if self.timer > totalSeconds:
                pygame.quit() 
                sys.exit() 

            self.advance(dt = dt)

        #print(positions)

    def draw(self, x, y, width, height, color, rotation=0):

        points = []

        # The distance from the center of the rectangle to
        # one of the corners is the same for each corner.
        radius = math.sqrt((height / 2)**2 + (width / 2)**2)

        # Get the angle to one of the corners with respect
        # to the x-axis.
        angle = math.atan2(height / 2, width / 2)

        # Transform that angle to reach each corner of the rectangle.
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]

        # Convert rotation from degrees to radians.
        rot_radians = (math.pi / 180) * rotation

        # Calculate the coordinates of each point.
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            points.append((x + x_offset, y + y_offset))

        pygame.draw.polygon(self.scene, color, points)

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
        print(self.s[0],self.s[1],self.timer) #for debugging

# program starts here
if __name__ == "__main__":

    vex = VexCar()
    vex.run(60)