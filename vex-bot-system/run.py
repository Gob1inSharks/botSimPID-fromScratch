#import matplotlib.pyplot as plt
#import numpy as np
#import random

import pygame
import sys
import os

#import math

from vex import VexCar
from botcontroller import Controller

import utils

TIME_START = 0
TIME_STOP = 60
TIME_INCREMENTS = 0.1

INITIAL_POSITION = 0
INITIAL_VELOCITY = 0

bot = VexCar()
control = Controller(bot)

def displayInitValues():

    values = f"""
--init values:
    target: {control.target}
    Kp: {control.Kp}
    Ki: {control.Ki}
    Kd: {control.Kd}"""

    print(values)
    return values

def printRunningValues():

    values=f"""
--timer: {bot.timer}
--bot values: 
    [in] V1 = {bot.V[0]},
    [in] V2 = {bot.V[1]},
    [out] angle = {bot.gyro}
--control values: 
    previous_step = {control.previous_step},
    current_step = {control.current_step},
    advanced_step = {control.advanced_step},
    all_steps = {control.all_steps}"""
    
    print(values)
    return values

def run(totalSeconds):

    #times = np.arange(0, totalSeconds, self.TICK)

    while True:

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit() 

        bot.scene.fill((35,35,35)) 

        bot.scene.blit(bot.assets['field'],(0,0))

        bot.drawCar(bot.SCENE_WIDTH//2 + bot.h,
                      (bot.s[0]+bot.s[1])//2,
                      100,100,(255,255,255),
                      rotation = bot.findCarAngle())
        
        bot.gyro = bot.findCarAngle()
            
        bot.drawLine()

        bot.screen.blit(pygame.transform.scale(bot.scene,(bot.SCREEN_WIDTH,bot.SCREEN_HEIGHT)), (0,0)) 

        pygame.display.update() 

        dt = bot.clock.tick(bot.FPS) * .001 

        bot.timer += dt

        if bot.timer > totalSeconds:
            pygame.quit() 
            sys.exit() 

        control.updateMotors()

        bot.advance(dt = dt)

        printRunningValues()

        #print(positions) #for debugging(

if __name__ == "__main__":

    control.Kp = 0.03
    control.Ki = 0.001
    control.Kd = 2

    control.target = 0

    #this is here to test the
    #versatility of PID controller
    bot.NOISE_MAGNITUDE = 12

    displayInitValues()
    run(TIME_STOP)