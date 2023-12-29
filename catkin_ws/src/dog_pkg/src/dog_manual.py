#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray, Bool
from sensor_msgs.msg import Joy
import math
from math import pi


jx = 0.
jy = 0.
theta = pi/2
speed = 80
state = 0
def joy_callback(msg):
    global speed, theta, jx, jy
    jx, jy = msg.axes[:2]
    jx = -jx
def state_callback(msg):
    global state
    state = msg.data

def dog_manual():
    global theta, speed, jx, jy, state
    theta = pi/2
    speed = 80
    rospy.init_node('dog_manual')
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    rospy.Subscriber("joy", Joy, joy_callback)
    rospy.Subscriber("state", Int32, state_callback)
    while not rospy.is_shutdown():
        if state == 2:
            ratio = math.sqrt(jx**2+jy**2)
            theta = math.atan2(jy,jx)
            # print(jx," ",jy)
            theta_pub.publish(float(theta))
            speed_pub.publish(int(speed*ratio))
        rospy.sleep(0.1)
if __name__ == '__main__':
    dog_manual()