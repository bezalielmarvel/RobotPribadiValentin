from pyglet.gl import *
from pyglet.window import key
from gl_lib.sim.geometrie.point import Point
import math

class Camera:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.cpt = 0

    def mouse_motion(self,dx,dy):

        """vitesse de la camera"""
        dx/=10
        dy/=10

        self.rot[0]-=dx

    def update(self,dt,keys):

        s = dt*10

        rotY = -self.rot[0]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        if keys[key.W]:
            self.pos[1]+=dx
            self.pos[2]-=dz
        if keys[key.S]:
            self.pos[1]-=dx
            self.pos[2]+=dz

    def updateCarre(self,dt,keys):

        s = dt*10

        rotY = -self.rot[0]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)

        self.avancer(dx,dz)
        if self.pos[2]>0:
            self.reculer(dx,dz)
            self.rot[0] += 1
            self.rot[0] += dx
            self.cpt = 1

        if self.rot[0] == 270 and self.cpt == 1:
            self.avancer(dx,dz)

        if self.pos[1]>20:
            self.cpt = 2

        if self.cpt == 2:
            self.reculer(dx,dz)
            self.rot[0] += 1
            self.rot[0] += dx
            self.cpt = 3

        if self.pos[2] < -10 and self.cpt == 3:
            self.reculer(dx,dz)
            self.rot[0] += 1
            self.rot[0] += dx

        if self.pos[1] < 10:
            self.cpt = 4

        if self.cpt == 4:
            self.rot[0] += 1
            self.rot[0] += dx

        if self.rot[0] > 450 and self.cpt == 4:
            self.reculer(dx,dz)
            self.cpt = 5

        if self.cpt == 5 and self.rot[0] > 540:
            self.reculer(dx,dz)

    def avancer(self,dx,dz):
        self.pos[1] += dx
        self.pos[2] -= dz

    def reculer(self,dx,dz):
        self.pos[1] -= dx
        self.pos[2] += dz



    def stop(self):
        self.pos[1] = self.pos[1]
        self.pos[2] = self.pos[2]

    def on_key_press(self,KEY,MOD):
       if KEY == key.SPACE:
            pyglet.image.get_buffer_manager().get_color_buffer().save('../../screenshot.png')