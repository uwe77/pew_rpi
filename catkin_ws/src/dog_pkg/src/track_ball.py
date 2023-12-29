#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray, Bool
from sensor_msgs.msg import Joy
import math
from math import pi


ball_x = 0
ball_y = 0
ball_r = 0
theta = pi/2
state = 0
speed = 50
BOUND_X = 640
BOUND_Y = 480

def state_callback(msg):
    global state
    state = msg.data

def ball_center_callback(msg):
    global ball_x, ball_y, ball_r, theta, speed, BOUND_X
    ball_x, ball_y, ball_r = msg.data[:3]

def track_ball():
    global ball_x, ball_y, ball_r, theta, speed, BOUND_X, state
    theta = pi/2
    speed = 0
    ball_x = 0
    ball_r = 0
    count = 0
    rospy.init_node('track_ball')
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    rospy.Subscriber('ball_center', Int32MultiArray, ball_center_callback)
    rospy.Subscriber("state", Int32, state_callback)
    while not rospy.is_shutdown():
        if state == 1:
            if ball_r != 0:
                if ball_r < 300:
                    theta = math.acos((ball_x-BOUND_X/2)/(BOUND_X/2))
                    if abs(abs(theta) - pi/2) <= pi/24:
                        speed = 100/340*(350-ball_r)
                        theta = pi/2
                    else:
                        speed = 50/340*(350-ball_r)
                else:
                    speed = 100
                    theta = pi/2
            else:
                speed = 0
                theta = pi/2
            theta_pub.publish(float(theta))
            speed_pub.publish(int(speed))

        rospy.sleep(0.1)
if __name__ == '__main__':
    track_ball()