import time
import math
from tkinter import *
from gl_lib.sim.affichage.d2.interface import AppRobot
from gl_lib.sim.robot.capteur.Capteur import Capteur
from gl_lib.sim.geometrie.point import *
from gl_lib.sim.robot import *
from gl_lib.sim.geometrie import *
from gl_lib.sim.affichage.d2.vue import *
from gl_lib.sim.robot.capteur import *

from PIL import Image

class Robot2I013sim(object):


    WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)
    
    def __init__(self,controler,fps=1):
        
        self.robotSim=RobotPhysique(Pave(100,200,0),Objet3D(),Objet3D(), Vecteur(-1,0,0))
        self.robotSim.deplacer(Vecteur(100,100,0))
        self.robotSim.tete = Tete(self.robotSim)
        self.cp = CapteurIR(self.robotSim.tete)
        self.a=Arene(700,[self.robotSim],700)
        self.robotSim.tete.lcapteurs = [self.cp]
        self.dist_rd = 0
        self.dist_rg = 0
        
        self.MOTOR_LEFT= "MOTOR_LEFT"
        self.MOTOR_RIGHT = "MOTOR_RIGHT"

        self.controler = controler

        self.fps=fps


    def run(self,verbose=True):
        
        if verbose:
            print("Starting ... (with %f FPS  -- %f sleep)" % (self.fps,1./self.fps))
        ts=time.time()
        tstart = ts
        cpt = 0
        
        try:
            while not self.controler.stop():
                ts = time.time()
                self.controler.update()
                time.sleep(1./self.fps)
                if verbose:
                    print("Loop %d, duree : %fs " % (cpt,time.time()-ts))
                cpt+=1
        except Exception as e:
            print("Erreur : ",e)
        self.stop()
        if verbose:
            print("Stoping ... total duration : %f (%f /loop)" % (time.time()-tstart,(time.time()-tstart)/cpt))

    def set_motor_dps(self, port, dps):
        if port == "MOTOR_LEFT":
            
            self.robotSim.tournerAutour(self.robotSim.rd.centre, dps)
        
        if port == "MOTOR_RIGHT":
            self.robotSim.tournerAutour(self.robotSim.rd.centre, -dps)
        if port == "MOTOR_LEFT+MOTOR_RIGHT" or port == "MOTOR_RIGHT+MOTOR_LEFT" :
            self.robotSim.avancer(1)


    def stop(self):
        """ Arrete le robot """
        print("stop")

