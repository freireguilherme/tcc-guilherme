import zmq
import time
import numpy as np
import spatialmath as sm
from easyEEZYbotARM.kinematic_model import EEZYbotARM_Mk2

#  função que recebe uma lista de dados string e formata num array float
def f_d (dado_str):
    values = []
    dado = dado_str.split('\n')
    for d in dado:
        dado_valor = d.split(", ")
        dado_valor = [float(valor) for valor in dado_valor]
        values.append(dado_valor)
    return values

#função que recebe envia para o server side as informações de junta
def set_active_joint_angle(socket, joint_angles):
    #mandar posições de junta para o coppelia
    socket.send(b"set_active_joint_angle")

    response = socket.recv()
    print(response.decode('utf-8'))
    joint_angles_str = ','.join(str(angle) for angle in joint_angles)

    socket.send(joint_angles_str.encode('utf-8'))

    # Aguardar uma resposta do servidor (opcional)
    response = socket.recv()
    print(response.decode('utf-8'))

    socket.send(b"get_active_joint_angle")

    #  Get the reply.
    joint_info_str = socket.recv()

    # Decodificar a sequência de bytes para uma string
    lista_valores = joint_info_str.decode('utf-8')
    lista_valores = f_d(lista_valores)
    print("Angulos das juntas no Coppelia (deg): motor1: {}, motor2: {}, motor3: {}, auxMotor1: {}".format(lista_valores[0][0], lista_valores[1][0], lista_valores[2][0], lista_valores[3][0]))

    socket.send(b"get_end_efector_position")
    EE_position_srt = socket.recv()
    EE_position = EE_position_srt.decode('utf-8')
    EE_position = f_d(EE_position)
    dado = []
    for valor in EE_position[0]:
        dado.append(valor*1000)
    print ("Posicao do efetuador final no Coppelia (mm) e x: {:.2f}, y:{:.2f}, z:{:.2f}".format(dado[0], dado[1], dado[2]))



context = zmq.Context()

#  Socket to talk to server
print("Connecting to CoppeliaSim server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


# initial joint angles
jointAngle1 = 0
jointAngle2 = 40
jointAngle3 = -100

# Create an EEZYbotARM Mk2 object
myRobotArm = EEZYbotARM_Mk2(jointAngle1, jointAngle2, jointAngle3)

x = +0.24881 * 1000 # mm
y = -0.04396 * 1000  # mm
z = +0.11799 * 1000  # mm

# Compute inverse kinematics
a1, a2, a3 = myRobotArm.inverseKinematics(x, y, z)
# Print the result
print('To move the end effector to the cartesian position (mm) x={}, y={}, z={}, the robot arm joint angles (degrees)  are q1 = {}, q2= {}, q3 = {}'.format(x, y, z, a1, a2, a3))

# Visualise the new joint angles
myRobotArm.updateJointAngles(q1=a1, q2=a2, q3=a3)

joint_angles = [a1, a2, -a3]

#mandar posições de junta para o coppelia
set_active_joint_angle(socket, joint_angles)
myRobotArm.plot()
