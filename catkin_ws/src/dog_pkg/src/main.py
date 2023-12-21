#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray
import math
from math import pi


ball_x = 0
ball_y = 0
theta = pi/2
speed = 50
BOUND_X = 640
BOUND_Y = 480
def ball_center_callback(msg):
    global ball_x, ball_y, theta, speed, BOUND_X
    ball_x = msg.data[0]
    ball_y = msg.data[1]
    theta = pi/2 - math.acos((ball_x-BOUND_X/2)/(BOUND_X/2))
    print(theta)
    if int(theta) == int(pi/2):
        speed = 100
    else:
        speed = 50
def main():
    global ball_x, ball_y, theta, speed, BOUND_X
    theta = pi/2
    speed = 0
    ball_x = 0
    rospy.init_node('main')
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    rospy.Subscriber('ball_center', Int32MultiArray, ball_center_callback)
    while not rospy.is_shutdown():
        print(speed)
        theta_pub.publish(float(theta*180/pi))
        speed_pub.publish(int(speed))
        rospy.sleep(0.1)
if __name__ == '__main__':
    main()