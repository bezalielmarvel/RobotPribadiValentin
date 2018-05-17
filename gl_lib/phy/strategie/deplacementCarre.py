from robot2I013 import Robot2I013
import time
import numpy as np
import math
#import matplotlib.pyplot as plt
class DeplacementCarre(object):
    def __init__(self):
        self.robot = Robot2I013(self)
        self.degre_init = self.robot.get_motor_position()[1]
        self.dist = 0
        self.set_speed(100,100)
        self.tour = 0
        self.distT = (90/360)*math.pi*Robot2I013.WHEEL_BASE_WIDTH
        self.stopF = False
        self.cmpt = 0

    def set_led(self,col):
        self.robot.set_led(self.robot.LED_LEFT_EYE+self.robot.LED_RIGHT_EYE,*col)
    def set_l_led(self,col):
        self.robot.set_led(self.robot.LED_LEFT_EYE,*col)
    def set_r_led(self,col):
        self.robot.set_led(self.robot.LED_RIGHT_EYE,*col)
    def set_speed(self,lspeed,rspeed):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT,lspeed)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT,rspeed)
    def turn_right(self,speed):
        self.set_speed(-speed,speed)
    def turn_left(self,speed):
        self.set_speed(speed,-speed)
    def forward(self,speed):
        self.set_speed(speed,speed)
    
    def update(self):
        #dss = min(255,int(self.robot.distance()/10))
        if self.tour == 0:
            self.dist = Robot2I013.WHEEL_CIRCUMFERENCE*(self.robot.get_motor_position()[1] - self.degre_init)/360
            print("Distance : ", self.dist," Position des roues :", self.robot.get_motor_position()[0], self.robot.get_motor_position()[1])
        
            if self.dist<300:
                self.set_speed(100,100)
            else:
                self.set_speed(0,0)
                self.dist = 0;
                self.degre_init = self.robot.get_motor_position()[1]
                self.tour = 1
        if self.tour == 1:
            self.dist = Robot2I013.WHEEL_CIRCUMFERENCE*(self.robot.get_motor_position()[1] - self.degre_init)/360
            if self.dist<self.distT:
                self.set_speed(-100,100)
            else:
                self.set_speed(0,0)
                self.dist = 0;
                self.degre_init = self.robot.get_motor_position()[1]
                self.tour = 0
                self.cmpt = self.cmpt+1
                if self.cmpt == 4:
                    self.stopF = True
    
        # plt.imshow(self.robot.get_image())

    def stop(self):
        return self.stopF
    
    def run(self):
        self.robot.run()


if __name__=="__main__":
    t = DeplacementCarre()
    t.run()

