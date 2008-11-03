from curves import *
from actions import *
from timelines import *
from numpy import *
from solidfuel.Math import Vector
from solidfuel.Logic import Event, Condition

# Verlet-style numerical integration
class Verlet(Curve):
    def __init__(self, start, startvalue, startvelocity, accelCurve):
        Curve.__init__(self, start)
        self._lastUpdate = self._start
        self._lastValue = startvalue - startvelocity
        self._curValue = startvalue
        self._accelCurve = accelCurve
        
    # non-destructive - we are testing what would happen if we moved this much forward in time
    def testValue(self, time, accelValue):
        elapsed = time - self._lastUpdate
        return self._curValue + (self._curValue - self._lastValue + accelValue * elapsed * elapsed)
        
    # destructive - this assumes we have actually moved forward in time
    def value(self, time):
        oldValue = self._curValue
        self._curValue = self.testValue(time, self._accelCurve.value(time))
        self._lastValue = oldValue
        return self._curValue

class Force(Action):
    def __init__(self, accelerator, startTime, length, magnitude):
        self._curve = ConstantCurve(startTime, magnitude, length)
        self._accelerator = accelerator
        Action.__init__(self, self._curve)
        
    def update(self, time):
        self._accelerator.applyForce(self._curve.value(time))

class Accelerator(Curve):
    def __init__(self, startTime, mass):
        Curve.__init__(self, startTime)
        self._forces = Timeline()
        self._mass = mass
        
    def value(self, time):
        self._curValue = array([0.0] * 3)
        self._forces.update(time)
        return self._curValue
        
    def addForce(self, startTime, length, magnitude):
        self._forces.addAction(Force(self, startTime, length, magnitude))
    
    def applyForce(self, magnitude):
        self._curValue += magnitude * self._mass
        
class PenetrationDetected:
    def __init__(self, body1, body2):
        self._body1 = body1
        self._body2 = body2
        
class Collision:
    def __init__(self, body1, body2, relativeVelocity, normal):
        self._body1 = body1
        self._body2 = body2
        self._relativeVelocity = relativeVelocity
        self._normal = normal

class CollisionDetectionGroup(list):
    def __init__(self, tolerance=0.001):
        list.__init__(self)
        self._tolerance = tolerance
        
    def getCollisions(self, time):
        
        def getCollisionsInner(positions, velocities, bodies):
            colliding = []
            
            if len(bodies) >= 2:
                body1 = bodies[0]
                for body2 in bodies[1:]:
                    r = body1._radius + body2._radius
                    d = Vector(positions[body1] - positions[body2])
                    s = d.norm()
                    
                    normal = d / s
                    relVel = velocities[body1] - velocities[body2]
                    vrn = relVel.dot(normal)
                    
                    if abs(s) <= self._tolerance and vrn < 0.0:
                        colliding.append(Collision(body1, body2, relVel, normal))
                    elif s < -self._tolerance:
                        raise PenetrationDetected(body1, body2)
                    
                colliding += getCollisionsInner(positions, velocities, bodies[1:])
            return colliding
            
        positions = {}
        velocities = {}
        for obj in self:
            (positions[obj], velocities[obj]) = obj.testPositionAndVelocity(time)
        colliding = getCollisionsInner(positions, velocities, self)
        return colliding
            
class RigidBody:
    def __init__(self, node, mass, radius, startVelocity=None):
        self._node = node
        self._startTime = 0.0
        self._radius = radius
        self._accelerator = Accelerator(self._startTime, mass)
        if startVelocity is None:
            startVelocity = array([0.0] * 3)
        self._verlet = Verlet(self._startTime, array([node.x, node.y, node.z]), startVelocity, self._accelerator)
        self._curves.append(self._verlet)
        
    def addForce(self, startTime, length, magnitude):
        self._accelerator.addForce(startTime, length, magnitude)
        
    def addConstantForce(self, magnitude):
        self._accelerator.addForce(0.0, None, magnitude)
        
    def testPositionAndVelocity(self, time):
        pos = self._verlet.testValue(time, self._accelerator.value(time))
        vel = (pos - array(self._node.x, self._node.y, self._node.z)) / (time - self._verlet.lastUpdate)
        return (pos, vel)
        
    def update(self, time):
        (self._node.x, self._node.y, self._node.z) = self._verlet.value(testTime)

class DynamicsSimulator(Action):
    def __init__(self):
        Action.__init__(self)
        self._collider = CollisionDetectionGroup()
        
    def addBody(self, body):
        self._collider.append(body)
        
    def removeBody(self, body):
        self._collider.remove(body)
        
    def update(self, time):
        tryAgain = True
        dtime = time - self._lastUpdate
        
        while tryAgain and dtime > 0.0:
            tryAgain = False
            testTime = self._lastUpdate + dtime
            
            try:
                collisions = self._collider.getCollisions(testTime)
            except PenetrationDetected:
                tryAgain = True
                dtime /= 2
            else:
                self._lastUpdate = testTime
                self.updated.trigger()
                for body in self._collider:
                    body.update(testTime)
                for collision in collisions:
                    collision.body1.
                    
