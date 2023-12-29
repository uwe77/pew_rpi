#!/usr/bin/python3
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image

import rospy
from std_msgs.msg import Int32

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

image_open = Image.open("/home/pew/pew_rpi/catkin_ws/src/oled_pkg/src/img/open_eye.jpg")
image_close = Image.open("/home/pew/pew_rpi/catkin_ws/src/oled_pkg/src/img/close_eye.jpg")
image_fire1 = Image.open("/home/pew/pew_rpi/catkin_ws/src/oled_pkg/src/img/fire1.jpg")
image_fire2 = Image.open("/home/pew/pew_rpi/catkin_ws/src/oled_pkg/src/img/fire2.jpg")

image_open = image_open.convert('1')
image_close = image_close.convert('1')
image_fire1 = image_fire1.convert('1')
image_fire2 = image_fire2.convert('1')
image_open = image_open.resize((width, height), Image.ANTIALIAS)
image_close = image_close.resize((width, height), Image.ANTIALIAS)
image_fire1 = image_fire1.resize((width, height), Image.ANTIALIAS)
image_fire2 = image_fire2.resize((width, height), Image.ANTIALIAS)

choice = '1'

def callback(data):
    global choice
    choice = str(data.data)
    print(choice)

def OLED_display():
    global choice
    state = 1
    rospy.init_node('OLED_display', anonymous=True)
    rospy.Subscriber("expression_choice", Int32, callback)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown(): 
        print("choice: ", choice)
        num = int(choice)
        if num == 1:
            if state == 1:
                disp.clear()
                disp.image(image_open)
                disp.display()
                state = -1 * state
            elif state == -1:
                disp.clear()
                disp.image(image_close)
                disp.display()
                state = -1 * state
        elif num == 2:
            if state == 1:
                disp.clear()
                disp.image(image_fire1)
                disp.display()
                state = -1 * state
            elif state == -1:
                disp.clear()
                disp.image(image_fire2)
                disp.display()
                state = -1 * state
        rate.sleep()
        disp.clear()

if __name__ == '__main__':
    try:
        OLED_display()
    except rospy.ROSInterruptException:
        pass
