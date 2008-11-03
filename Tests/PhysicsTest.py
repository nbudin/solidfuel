from solidfuel.Graphics import *
from solidfuel.Controllers import *
from numpy import *
import pygame
from pygame.locals import *
from ctypes import *

pygame.init()
d = Display(640, 480)
scene = ThreeDScene()
d.addChild(scene)
light1 = Light()
light1.x = 6
light2 = Light()
light2.z = 6
light2.x = -3
scene.addLight(light1)
scene.addLight(light2)

ball = Sphere(0.25)
ball.x = -2.0
scene.addChild(ball)

t = Timeline()
sim = DynamicsSimulator()
sim.setGravity(0, 0, 0)
g = ode.dCreateSphere(sim._space, dReal(0.25))
mass = dMass()
ode.dMassSetSphere(byref(mass), 1, dReal(0.25))
dyn = sim.makeDynamic(ball, g, mass)

#floor = ode.GeomPlane(sim._space, (0, -2, 0), 0)
t.addAction(sim)

#ballMotion = RigidBodyMotion(ball, 1.0, array([0.005, 0.005, 0.0]))
#ballMotion.addConstantForce(array([0.0, -0.0001, 0.0])) #gravity
#t.addAction(ballMotion)

e = pygame.event.poll()
startTime = pygame.time.get_ticks() / 1000.0
while e.type != QUIT:
    d.render()
    t.update(pygame.time.get_ticks() / 1000.0 - startTime)
    e = pygame.event.poll()