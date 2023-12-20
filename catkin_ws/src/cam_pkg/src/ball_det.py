#!/usr/bin/env python3
import numpy as np
import cv2
import time, os
import rospy
from std_msgs.msg import Int32MultiArray


BOUND_X = 800
BOUND_Y = 600
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            '../../../images')
FILE_NAME = "vision"

def main():
    rospy.init_node('ball_det')
    ball_pos_pub = rospy.Publisher('ball_center', Int32MultiArray, queue_size=1)
    count = 1
    while not rospy.is_shutdown():
        print(count)
        try:

            filename = f'{FILE_NAME}{count}.png'
            captured_frame = cv2.imread(os.path.join(IMAGE_PATH,filename), cv2.IMREAD_UNCHANGED)
            if captured_frame is None:
                raise Exception("Image not found")
            captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR) # Convert original image to BGR, since Lab is only available from BGR
            captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3) # First blur to reduce noise prior to color space conversion
            captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab) # Convert to Lab color space, we only need to check one channel (a-channel) for red here
            captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
            captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2) # Second blur to reduce more noise, easier circle detection
            circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60) # Use the Hough transform to detect circles in the image
            if circles is not None:
                print("circles detected!!")
                circles = np.round(circles[0, :]).astype("int")
                pos_msg = Int32MultiArray()
                pos_msg.data = [circles[0, 0], circles[0, 1]]
                ball_pos_pub.publish(pos_msg)
            if count >= 10:
                count = 0
            count += 1
        except:
            pass
        rospy.sleep(0.02)
if __name__ == '__main__':
    main()