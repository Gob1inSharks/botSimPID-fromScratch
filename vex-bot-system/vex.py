"""
Author: Not Goblinsharks
Comments:

    This is a simulation of a vex drivetrain that can be controlled by the user.

    And it is the biggest piece of shit I have ever coded

    TODO: Clean this crap up

    TODO: The bot's angle isn't rendering as tangental to the line
    This is obivous when you run the program

    TODO: ADD ACCERLATION
    This is a problem 
    
    TODO: ADD BRAKE        

"""
import random
import numpy as np
import pygame
import os
import sys
import math

random.seed(2049)

DIR = os.path.dirname(os.path.realpath(__file__))

BASE_IMAGE_PATH = '/assets/images' 
BASE_SETTINGS_PATH = '/assets/jsons'
DELETING_SUBDIRECTORIES = ['/__pycache__','/temp']
COLOUR_KEY = (0,0,0) #black

def load_image(path): 

    """
    This function loads an image from the specified path and sets the color key for transparency.

    Parameters:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The loaded image with the color key set for transparency.
    """

    image = pygame.image.load(DIR+BASE_IMAGE_PATH+'/'+path).convert() 
    image.set_colorkey(COLOUR_KEY)

    return image 

class VexCar:

    def __init__(self,controller = None):

        self.MAX_SPEED = 200

        self.theta = 0

        self.NOISE_MAGNITUDE = 4

        self.MASS = 10
        
        self.s = [0,0]
        self.h = 0
        self.v = [0,0]
        self.V = [12,12]

        self.previous = [0,0,0,0]

        self.RADIUS_RIGHT = 5
        self.RADIUS_LEFT  = 7

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
        
    def vol2speed(self,V,radius = 1):

        rpm = 34 * V

        if rpm > self.MAX_RPM:
            rpm = self.MAX_RPM
        elif rpm < 0:
            rpm = 0

        return (2*np.pi*radius) * rpm / 60

    def run(self,totalSeconds):

        times = np.arange(0, totalSeconds, self.TICK)

        while True:

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 

            self.scene.fill((35,35,35)) 

            self.scene.blit(self.assets['field'],(0,0))

            self.drawCar(self.SCENE_WIDTH//2 + self.h,
                      (self.s[0]+self.s[1])//2,
                      100,100,(255,255,255),
                      rotation = self.findCarAngle())
            
            self.drawLine()

            self.screen.blit(pygame.transform.scale(self.scene,(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)), (0,0)) 

            pygame.display.update() 

            dt = self.clock.tick(self.FPS) * .001 

            self.timer += dt

            if self.timer > totalSeconds:
                pygame.quit() 
                sys.exit() 

            self.advance(dt = dt)

        #print(positions) #for debugging(

    def getXY(self):

        return (max(self.s[0],self.s[1]),
                self.SCENE_WIDTH//2+self.h)

    def findCarAngle(self):

        return math.atan2(self.h,max(self.s[0],self.s[1]))*180/math.pi

    def drawCar(self, x, y, width, height, color, rotation=0):

        points = []

        radius = math.sqrt((height / 2)**2 + (width / 2)**2)

        angle = math.atan2(height / 2, width / 2)

        angles = [angle, -angle + math.pi, angle + math.pi, -angle]

        rot_radians = (math.pi / 180) * rotation

        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            points.append((x + x_offset, y + y_offset))

        pygame.draw.polygon(self.scene, color, points)

    def drawLine(self, width = 1):

        pygame.draw.line(self.assets["field"],
                          (255,255,0), 
                         
                         ((self.SCENE_WIDTH//2 + self.previous[3]),
                          (self.previous[0]+self.previous[1])/2), 

                          ((self.SCENE_WIDTH//2 + self.h),
                          (self.s[0]+self.s[1])/2), 
                
                          width)

    def advance(self,dt = 0.1):

        self.previous = [self.s[0],self.s[1],self.findCarAngle(),self.h]

        self.v[0] = self.vol2speed(self.V[0],radius=self.RADIUS_RIGHT)
        self.v[1] = self.vol2speed(self.V[1],radius =self.RADIUS_LEFT)

        if self.v[0] > self.MAX_SPEED:
            self.v[0] = self.MAX_SPEED
        elif self.v[0] < -self.MAX_SPEED:
            self.v[0] = -self.MAX_SPEED

        if self.v[1] > self.MAX_SPEED:
            self.v[1] = self.MAX_SPEED
        elif self.v[1] < -self.MAX_SPEED:
            self.v[1] = -self.MAX_SPEED

        self.v[0] -= random.randint(int(self.NOISE_MAGNITUDE*500), int(self.NOISE_MAGNITUDE*1000))/1000
        #self.v[1] -= random.randint(0, int(self.NOISE_MAGNITUDE*1000))/1000

        self.s[0] += self.v[0]*dt
        self.s[1] += self.v[1]*dt

        # todo clean this up
        self.h -= (self.s[1]-self.s[0]) #add a horizontal component to the car

        #print(self.v[0],self.v[1]) #for debugging
        print(self.s[0],self.s[1],self.findCarAngle()) #for debugging

# program starts here
if __name__ == "__main__":

    vex = VexCar()
    vex.run(60)