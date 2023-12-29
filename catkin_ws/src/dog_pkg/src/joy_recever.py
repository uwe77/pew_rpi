#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray, Bool
from sensor_msgs.msg import Joy
import math
from math import pi
import sys, os, time

file_path = "../../../log/state.txt"
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            file_path)
state = 0
count = 0
face = 1
def joy_callback(msg):
    global state, count, face, file_path
    if msg.buttons[2] == 1 and msg.buttons[3] == 0 and msg.buttons[4] == 0:
        state = 1
    elif msg.buttons[2] == 0 and msg.buttons[3] == 1 and msg.buttons[4] == 0:
        state = 2
    elif msg.buttons[2] == 0 and msg.buttons[3] == 0 and msg.buttons[4] == 1:
        state = 0
    if msg.buttons[2] == 1 or msg.buttons[3] == 1 or msg.buttons[4] == 1:
        init_size = os.path.getsize(file_path)
        while True:
            time.sleep(0.02)
            current_size = os.path.getsize(file_path)
            if current_size == init_size:
                break
            init_size = current_size
        try:
            with open(file_path, 'w') as file:
                file.write(f'{state}')
        except:
            pass
        
    if msg.buttons[0] == 1:
        if count == 0:
            count += 1
    else:
        if count == 1:
            count += 1
            face = (face%2)+1
def joy_recever():
    global state, count, face
    state = 0
    count = 0
    face = 1
    rospy.init_node('joy_recever')
    state_pub = rospy.Publisher('state', Int32, queue_size=1)
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    face_pub = rospy.Publisher('expression_choice', Int32, queue_size=1)
    rospy.Subscriber("joy", Joy, joy_callback)
    while not rospy.is_shutdown():
        if state == 0:
            speed_pub.publish(int(0))
            theta_pub.publish(float(pi/2))
        state_pub.publish(state)
        if count == 2:
            face_pub.publish(face)
            count = 0
        rospy.sleep(0.1)
if __name__ == '__main__':
    joy_recever()