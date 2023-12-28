#!/usr/bin/env python3
import numpy as np
import cv2
import os, time
import rospy
from std_msgs.msg import Int32MultiArray

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../../../images')
FILE_NAME = "vision"
lower_pink = np.array([140, 100, 50]) # 140 100 50
upper_pink = np.array([170, 255, 255]) # 170, 255, 255

def main():
    rospy.init_node('ball_det')
    ball_pos_pub = rospy.Publisher('ball_center', Int32MultiArray, queue_size=1)
    count = 0
    min_R = 10
    max_R = 150
    last_R = 0
    while not rospy.is_shutdown():
        try:
            count = (count % 2) + 1
            filename = f'{os.path.join(IMAGE_PATH, FILE_NAME)}{count}.png'
            init_size = os.path.getsize(filename)
            while True:
                time.sleep(0.02)
                current_size = os.path.getsize(filename)
                if current_size == init_size:
                    break
                init_size = current_size
            captured_frame = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            # captured_frame = cv2.rotate(captured_frame, cv2.ROTATE_180)
            captured_frame = cv2.resize(captured_frame, (640, 480))  # Downsize the image
            captured_frame_hsv = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space
            mask = cv2.inRange(captured_frame_hsv, lower_pink, upper_pink)
            mask = cv2.GaussianBlur(mask, (5, 5), 2)
            # cv2.imwrite("../../../images/mask.png", mask)
            level = last_R // 100
            if level == 0:
                min_R = 20
                max_R = 200
            elif level == 1:
                min_R = 50
                max_R = 250
            elif level == 2:
                min_R = 150
                max_R = 350
            elif level >= 3:
                min_R = 250
                max_R = 450
            circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=2, minDist=mask.shape[0] / 8,
                                    param1=100, param2=18, minRadius=min_R, maxRadius=max_R)
            pos_msg = Int32MultiArray()
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                pos_msg.data = [circles[0, 0], circles[0, 1], circles[0, 2]]
                last_R = circles[0, 2]
            else:
                pos_msg.data = [0, 0, 0]
                last_R = 0
            ball_pos_pub.publish(pos_msg)
        except:
            pass
        rospy.sleep(0.01)  # Adjust sleep time as needed

if __name__ == '__main__':
    main()
