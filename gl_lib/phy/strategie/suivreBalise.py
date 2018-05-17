from robot2I013 import Robot2I013
from detecteBalise import DetecteBalise
import time
import numpy as np
import math

class SuivreBalise():
    def __init__(self):
        self.robot = Robot2I013(self, fps=25.0)

        self.set_speed(0,0)
        self.stopF = False
        self.prog = 0
    
        self.image_tmp = self.robot.get_image()
        self.image_tmp.rotate(180)
        self.angle = DetecteBalise(self.image_tmp).angle_balise()


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

        # detecter la balise
        if self.cmpt % 25 == 0:
            self.image_tmp = self.robot.get_image()
            self.image_tmp.rotate(180)
            self.angle = DetecteBalise(self.image_tmp).angle_balise()
        
        # balise non detecte ou obstacle devant => ne pas bouger
        if self.angle == False or self.robot.get_distance() <= 15:
            self.prog = 0
        
        # balise detecte et pas de obstacle => choisir un progromme: tourner gauche, droite ou avancer
        else:
            self.dist_cour = 0;
            self.degre_init = abs(self.robot.get_motor_position()[1])
            self.dist_max_tourner = (abs(self.angle)/360)*math.pi*Robot2I013.WHEEL_BASE_WIDTH
            
            if self.angle > 5:
                self.prog = 1
            elif self.angle < -5:
                self.prog = 2
            else:
                self.prog = 3

         ## programmes:
         # ne pas bouger
        if self.prog == 0:
            self.forward(0)
            self.set_led(255,0,0) # led rouge
         # tourner a droite sur un angle exact
        elif self.prog == 1:
            self.set_l_led(255,255,0) # led jaune
            self.dist_cour = Robot2I013.WHEEL_CIRCUMFERENCE*(abs(self.robot.get_motor_position()[1]) - self.degre_init)/360
            self.turn_right(100)
            if self.dist_cour >= self.dist_max_tourner:
                self.forward(0)
                self.prog = 3
        # tourner a droite sur un angle exact
        elif self.prog == 2:
            self.set_r_led(255,255,0) # led jaune
            self.dist_cour = Robot2I013.WHEEL_CIRCUMFERENCE*(abs(self.robot.get_motor_position()[1]) - self.degre_init)/360
            self.turn_left(100)
            if self.dist_cour >= self.dist_max_tourner:
                self.forward(0)
                self.prog = 3
        # avancer
        elif self.prog == 3:
            self.forward(100)
            self.set_led(0,255,0)  # led vert
            

    def stop(self):
        return self.stopF
    
    def run(self):
        self.robot.run()


if __name__=="__main__":
    t = SuivreBalise()
    t.run()

