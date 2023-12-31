#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, String, Float32
import math


left_speed = 0
right_speed = 0
current_speed = 0
def dog_move_dir_callback(msg):
    global left_speed, right_speed, current_speed
    left_speed = int(current_speed*(math.sin(msg.data) + math.cos(msg.data)))
    right_speed = int(current_speed*(math.sin(msg.data) - math.cos(msg.data)))

def dog_move_speed_callback(msg):
    global current_speed
    current_speed = msg.data

def main():
    global left_speed, right_speed
    rospy.init_node('dog_legs')
    rospy.Subscriber('dog_move_dir', Float32, dog_move_dir_callback)
    rospy.Subscriber('dog_move_speed', Int32, dog_move_speed_callback)
    left_leg_pub = rospy.Publisher('motor_v_left', Int32, queue_size=1)
    right_leg_pub = rospy.Publisher('motor_v_right', Int32, queue_size=1)
    while not rospy.is_shutdown():
        left_leg_pub.publish(left_speed)
        right_leg_pub.publish(right_speed)
        rospy.sleep(0.01)

if __name__ == '__main__':
    main()