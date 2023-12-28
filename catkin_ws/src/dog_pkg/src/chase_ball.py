#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Int32MultiArray, Bool
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
ball_catch = False
def ball_center_callback(msg):
    global ball_x, ball_y, ball_r, theta, last_theta, speed, BOUND_X
    ball_x, ball_y, ball_r = msg.data[:3]

def track_ball():
    global ball_x, ball_y, ball_r, theta, speed, BOUND_X, last_theta, ball_catch
    theta = pi/2
    speed = 0
    ball_x = 0
    ball_r = 0
    ball_catch = False
    count = 0
    rospy.init_node('chase_ball')
    speed_pub = rospy.Publisher('dog_move_speed', Int32, queue_size=1)
    theta_pub = rospy.Publisher('dog_move_dir', Float32, queue_size=1)
    catch_pub = rospy.Publisher('dog_catch_ball', Bool, queue_size=1)
    rospy.Subscriber('ball_center', Int32MultiArray, ball_center_callback)
    while not rospy.is_shutdown():
        if ball_r != 0 and not ball_catch:
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
                ball_catch = True
        elif ball_r == 0 and not ball_catch:
            speed = 10
            oper = (last_theta - pi / 2) / abs(last_theta - pi / 2) if last_theta != pi / 2 else 1
            theta = (oper + 1)*pi/2
        
        if ball_catch:
            if count >= 5:
                catch_pub.publish(ball_catch)
                theta = 0
                speed = 10
                if ball_r != 0:
                    count = 0
                    ball_catch = False
            else:
                count += 1
        else:
            catch_pub.publish(ball_catch)

        print(theta*180/pi, speed, ball_r, ball_catch)
        theta_pub.publish(float(theta))
        last_theta = theta
        speed_pub.publish(int(speed))
        
        rospy.sleep(0.1)
if __name__ == '__main__':
    track_ball()