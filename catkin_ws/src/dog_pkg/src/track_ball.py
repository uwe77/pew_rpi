#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray
import math
from math import pi


ball_x = 0
ball_y = 0
ball_r = 0
theta = pi/2
last_theta = 0
speed = 50
BOUND_X = 640
BOUND_Y = 480
def ball_center_callback(msg):
    global ball_x, ball_y, ball_r, theta, last_theta, speed, BOUND_X
    if msg.data[2] != 0:
        ball_x, ball_y, ball_r = msg.data[:3]
        theta = math.acos((ball_x-BOUND_X/2)/(BOUND_X/2))
        if abs(abs(theta) - pi/2) <= pi/24:
            # if ball_r < 200:
            #     speed = 100/199 * (200 - ball_r)
            # else:
            #     speed = 0
            speed = 100/270*(300-ball_r) if ball_r < 200 else 0
            theta = pi/2
        else:
            speed = 50/270*(300-ball_r) if ball_r < 200 else 0
    else:
        speed = 10
        oper = (last_theta - pi / 2) / abs(last_theta - pi / 2) if last_theta != pi / 2 else 1
        theta = (oper + 1)*pi/2
    print(theta*180/pi, speed, msg.data[2])
def main():
    global ball_x, ball_y, theta, speed, BOUND_X, last_theta
    theta = pi/2
    speed = 0
    ball_x = 0
    rospy.init_node('track_ball')
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    rospy.Subscriber('ball_center', Int32MultiArray, ball_center_callback)
    while not rospy.is_shutdown():
        theta_pub.publish(float(theta))
        last_theta = theta
        speed_pub.publish(int(speed))
        rospy.sleep(0.1)
if __name__ == '__main__':
    main()