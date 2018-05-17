from gl_lib.sim.robot.strategie.deplacement.StrategieDeplacement import StrategieDeplacement
from gl_lib.sim.robot import *

class DeplacementSimple(StrategieDeplacement):
    def __init__(self, robot):
        """
        initialisation avec la classe mere
        """
        StrategieDeplacement.__init__(self, robot)
        
    def deplacementVers(self, destination):
        """
        le robot excute un mouvement de rotation, puis avance vers la destination
        """

        v=(destination-self.robot.forme.centre).toVect()
        distance=v.getNorme()
        diffAngle=self.robot.direction.getAngle2D()-v.getAngle2D()
        if distance>10:
            if abs(diffAngle)>0.1:
                self.robot.tourner(diffAngle)
            else :
                self.robot.avancer(1)
        else:
            self.robot.destination=None




    def deplacementRel(self, vecteur):
        """
        le robot excute un mouvement direct vers la destination indiquee par vecteur
        """
        self.deplacementVers(self.robot.centre+vecteur)
