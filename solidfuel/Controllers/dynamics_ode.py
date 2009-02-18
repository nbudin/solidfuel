from actions import *
from ctypes.util import find_library
from ctypes import *
import sys, os, atexit

if sys.platform == 'win32':
    ode = CDLL(find_library("ode.dll"))
else:
    ode = CDLL(find_library("ode"))
    
ode.dInitODE()
atexit.register(ode.dCloseODE)

dReal = c_float
dVector3 = dReal * 3
dVector4 = dReal * 4
dMatrix3 = dReal * (4 * 3)
dMatrix4 = dReal * (4 * 4)
dMatrix6 = dReal * (8 * 6)
dQuaternion = dReal * 4

dContactMu2           = 0x001
dContactFDir1         = 0x002
dContactBounce        = 0x004
dContactSoftERP       = 0x008
dContactSoftCFM       = 0x010
dContactMotion1       = 0x020
dContactMotion2       = 0x040
dContactMotionN       = 0x080
dContactSlip1         = 0x100
dContactSlip2         = 0x200

dContactApprox0       = 0x0000
dContactApprox1_1     = 0x1000
dContactApprox1_2     = 0x2000
dContactApprox1       = 0x3000

dGeomID = c_void_p

class dMass(Structure):
    _fields_ = [("mass", dReal),
                ("c", dVector4),
                ("I", dMatrix3)]
                
class dSurfaceParameters(Structure):
    _fields_ = [("mode", c_int),
                ("mu", dReal),
                ("mu2", dReal),
                ("bounce", dReal),
                ("bounce_vel", dReal),
                ("soft_erp", dReal),
                ("soft_cfm", dReal),
                ("motion1", dReal),
                ("motion2", dReal),
                ("motionN", dReal),
                ("slip1", dReal),
                ("slip2", dReal)]

class dContactGeom(Structure):
    _fields_ = [("pos", dVector3),
                ("normal", dVector3),
                ("depth", dReal),
                ("g1", dGeomID),
                ("g2", dGeomID),
                ("side1", c_int),
                ("side2", c_int)]

class dContact(Structure):
    _fields_ = [("surface", dSurfaceParameters),
                ("geom", dContactGeom),
                ("fdir1", dVector3)]
                
NEAR_CALLBACK = CFUNCTYPE(c_void_p, dGeomID, dGeomID)

class DynamicObject:
    def __init__(self, node, simulator):
        self._node = node
        self._simulator = simulator
        self._body = ode.dBodyCreate(self._simulator._world)
        ode.dBodySetPosition(self._body, dReal(self._node.x), dReal(self._node.y), dReal(self._node.z))
        
    def setGeom(self, geom):
        self._geom = geom
        ode.dGeomSetBody(geom, self._body)
        
    def setMass(self, mass):
        self._mass = mass
        ode.dBodySetMass(self._body, byref(self._mass))
        
    def updatePosition(self):
        (self._node.x, self._node.y, self._node.z) = ode.dBodyGetPosition(self._body)
        
    def updateRotation(self):
        pass
        

class DynamicsSimulator(Action):
    NEXTSPACE = 0
    NEXTJOINTGROUP = 0
    def __init__(self):
        Action.__init__(self)
        self._world = ode.dWorldCreate()
        self._space = ode.dHashSpaceCreate(DynamicsSimulator.NEXTSPACE)
        DynamicsSimulator.NEXTSPACE += 1
        self._contactGroup = ode.dJointGroupCreate(DynamicsSimulator.NEXTJOINTGROUP)
        DynamicsSimulator.NEXTJOINTGROUP += 1
        self._objs = []
        self._collideCB = NEAR_CALLBACK(self._collided)
        
    def __del__(self):
        ode.dJointGroupDestroy(self._contactGroup)
        ode.dSpaceDestroy(self._space)
        ode.dWorldDestroy(self._world)
        
    def setGravity(self, x, y, z):
        ode.dWorldSetGravity(self._world, x, y, z)
        
    def start(self):
        return 0.0
        
    def end(self):
        return None
        
    def length(self):
        return None
    
    def makeDynamic(self, node, geom, mass):
        obj = DynamicObject(node, self)
        obj.setGeom(geom)
        obj.setMass(mass)
        self._objs.append(obj)
        return obj
        
    def _collided(self, args, geom1, geom2):
        b1 = ode.dGeomGetBody(geom1)
        b2 = ode.dGeomGetBody(geom2)
        contact = dContact()
        contact.surface.mode = dContactBounce | dContactSoftCFM
        contact.surface.mu = 9000.0
        contact.surface.bounce = 0.9
        contact.surface.bounce_vel = 0.1
        contact.surface.soft_cfm = 0.001
        
        numc = ode.dCollide(geom1, geom2, 1, byref(contact.geom), sizeof(dContact))
        if numc:
            c = ode.dJointCreateContact(self._world, self._contactGroup, byref(contact))
            ode.dJointAttach(c, b1, b2)
        
    def update(self, time):
        n = 1
        dt = (time - self._lastUpdate) / n
        if dt <= 0.0:
            return
            
        for i in range(n):
            ode.dSpaceCollide(self._space, 0, self._collideCB)
            ode.dWorldQuickStep(self._world, dt)
            ode.dJointGroupEmpty(self._contactGroup)
        
        for obj in self._objs:
            obj.updatePosition()
            obj.updateRotation()
                
        Action.update(self, time)