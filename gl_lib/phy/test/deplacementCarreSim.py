from robot2I013sim import Robot2I013sim as Robot2I013
import time
import math
#import matplotlib.pyplot as plt
class DeplacementCarreSim(object):
    def __init__(self):
        self.robot = Robot2I013(self)
#        self.degre_init = self.robot.get_motor_position()[1]
        self.dist = 0
#        self.set_speed(100,100)
        self.tour = 0
        self.distT = (90/360)*math.pi*Robot2I013.WHEEL_BASE_WIDTH
        self.stopF = False
        self.cmpt = 0
        print(self.robot.robotSim.centre)
        print(self.robot.robotSim.rd.centre)
        print(self.robot.robotSim.rg.centre)

#    def set_speed(self,lspeed,rspeed):
#        self.robot.set_motor_dps(self.robot.MOTOR_LEFT,lspeed)
#        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT,lspeed)
#    def turn_right(self,speed):
#        self.set_speed(-speed,speed)
#    def turn_left(self,speed):
#        self.set_speed(speed,-speed)

    def update(self):
        if self.cmpt < 4:
            self.robot.set_motor_dps(self.robot.MOTOR_LEFT+self.robot.MOTOR_RIGHT,100)
            print(self.robot.robotSim.centre)
            self.cmpt += 1
        else:
            self.stopF = True

    def stop(self):
        return self.stopF
    
    def run(self):
        self.robot.run()

if __name__=="__main__":
    t = DeplacementCarreSim()
    t.run()

