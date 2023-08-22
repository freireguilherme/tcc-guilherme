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