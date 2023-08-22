import zmq
import numpy as np
import spatialmath as sm
import roboticstoolbox as rtb



context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response

print("Sending request ...")
# socket.send(b"Hello")
socket.send(b"get_active_joint_angle")

#  Get the reply.
# message = socket.recv()
joint_angles_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = joint_angles_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nAngulos das juntas ativas\n")
print(lista_valores)
#angulos em radianos
#motor1
angulo_junta1 = lista_valores[0]
#motor2
angulo_junta2 = lista_valores[1]
#motor3
angulo_junta3 = lista_valores[2]

socket.send(b"get_active_joint_position")
joint_position_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = joint_position_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nPosições das juntas ativas")
print(lista_valores)

#posicoes em x, y, z
#motor1
posicao_junta1 = lista_valores[0]
#motor2
posicao_junta2 = lista_valores[1]
#motor3
posicao_junta3 = lista_valores[2]

socket.send(b"get_active_joint_orientation")
joint_orientation_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = joint_orientation_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nOrientaçao das juntas ativas")
print(lista_valores)
#orientacao em alpha, beta, gamma em radianos
#motor1
orientacao_junta1 = lista_valores[0]
#motor2
orientacao_junta2 = lista_valores[1]
#motor3
orientacao_junta3 = lista_valores[2]


socket.send(b"get_active_links_info")
link_info_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = link_info_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nTamanho dos elos ativos")
print(lista_valores)
print("\n")
#tamanhos em x, y, z
#link1
tamnho_link1_atv = lista_valores[0]
#link2
tamnho_link2_atv = lista_valores[1]
#link3
tamnho_link3_atv = lista_valores[2]
#link4
tamnho_link4_atv = lista_valores[3]

print("Sending request ...")
# socket.send(b"Hello")
socket.send(b"get_passive_joint_angle")

#  Get the reply.
# message = socket.recv()
joint_angles_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores = joint_angles_str.decode('utf-8')
print("\nAngulos das juntas passivas\n")
print(lista_valores)
#angulo em radianos
angle_auxJoint0 = lista_valores[0]
angle_auxJoint1 = lista_valores[1]
angle_auxJoint3 = lista_valores[2]
angle_auxJoint4 = lista_valores[3]
angle_auxJoint7 = lista_valores[4]
angle_auxJoint8 = lista_valores[5]
angle_auxMotor1 = lista_valores[6]
angle_auxMotor2 = lista_valores[7]

socket.send(b"get_passive_joint_position")
joint_position_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = joint_position_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nPosições das juntas passivas")
print(lista_valores)
#posicao em x, y, z
posicao_auxJoint0 = lista_valores[0]
posicao_auxJoint1 = lista_valores[1]
posicao_auxJoint3 = lista_valores[2]
posicao_auxJoint4 = lista_valores[3]
posicao_auxJoint7 = lista_valores[4]
posicao_auxJoint8 = lista_valores[5]
posicao_auxMotor1 = lista_valores[6]
posicao_auxMotor2 = lista_valores[7]


socket.send(b"get_passive_joint_orientation")
joint_orientation_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = joint_orientation_str.decode('utf-8')
lista_valores = lista_valores_str.split("\n")
print("\nOrientaçao das juntas passivas")
print(lista_valores)
#orientação em alpha, beta, gamma (rad)
orientacao_auxJoint0 = lista_valores[0]
orientacao_auxJoint1 = lista_valores[1]
orientacao_auxJoint3 = lista_valores[2]
orientacao_auxJoint4 = lista_valores[3]
orientacao_auxJoint7 = lista_valores[4]
orientacao_auxJoint8 = lista_valores[5]
orientacao_auxMotor1 = lista_valores[6]
orientacao_auxMotor2 = lista_valores[7]

socket.send(b"get_passive_links_info")
link_info_str = socket.recv()
#print("Received reply %s [ %s ]" % (request, joint_info_str))
    
# Decodificar a sequência de bytes para uma string
lista_valores_str = link_info_str.decode('utf-8')
lista_valores = formatar_dado(lista_valores_str)



print("\nTamanho dos elos passivos")
print(lista_valores)
print("\n")
#tamanho em X, y, z
tam_auxLink0 = lista_valores[0]
tam_auxLink1 = lista_valores[1]
tam_auxLink2 = lista_valores[2]
tam_auxLink3 = lista_valores[3]
tam_auxLink4 = lista_valores[4]

#agora q tenhos as dimenções, monto o robot por  DH
print(tam_auxLink4[2])
