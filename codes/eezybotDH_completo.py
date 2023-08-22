import numpy as np
from numpy import pi
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3
from spatialmath import base


class EEzybot(DHRobot):

    def __init__(self, symbolic=False):
        if symbolic:
            import spatialmath.base.symbolic as sym

            zero = sym.zero()
            pi = sym.pi()
        else:
            from math import pi
        L= [
            RevoluteDH(a=0.0030),                                       #motor1
            RevoluteDH(d=0.0694, a=0.0350, alpha=-pi/2),                #motor1->auxJoint1
            RevoluteDH(d=0.0524, a=0.0030, alpha=-pi/2),                #motor1->motor3
            RevoluteDH(d=0.0524, a=0.0030, alpha=-pi/2),                #motor1->motor2
            RevoluteDH(d=0, a=0.1303, alpha=0),                         #motor2->auxJoint7
            RevoluteDH(a=0.0447),                                       #auxJoint7->auxJoint0
            RevoluteDH(d=0, a=0.1303, alpha=0),                         #motor2->auxJoint1
            RevoluteDH(a=0.0581),                                       #auxJoint1->auxJoint3
            RevoluteDH(a=0.1344),                                       #auxJoint4->auxJoint4
            RevoluteDH(a=0.1453),                                       #auxJoint1->auxMotor2
            RevoluteDH(a=0.0439),                                       #auxMotor2->auxJoint8
            ]
        super().__init__(
            L,
            name="EEzybotArm",
            manufacturer="daGzimo",
            #keywords=("dynamics", "symbolic", "mesh"),
            #symbolic=symbolic,
            #meshdir="meshes/UNIMATE/puma560",
            )
        
        """
            qz, zero joint angle configuration, ‘L’ shaped configuration

            qr, vertical ‘READY’ configuration

            qs, arm is stretched out in the x-direction

            qn, arm is at a nominal non-singular configuration
        """
        self.qr = np.array([0, 0, pi / 3])
        self.qz = np.zeros(3)

        # nominal table top picking pose
        self.qn = np.array([0, pi / 4, pi * (5 / 36),]) #0, 45, 25

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)
        self.addconfiguration("qn", self.qn)

if __name__ == "__main__":  # pragma nocover

    eezybot = EEzybot(symbolic=False)
    qr = np.array([0.0, 0.0, 0.0, pi / 2, 0.0, 0.0, -pi/2, 0, 0, 0, 0])
    print((eezybot.n))
    eezybot.plot(qr, block=True)
    print(eezybot.ets())
