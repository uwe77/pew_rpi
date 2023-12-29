import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time

from PIL import Image

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

image_open = Image.open("/img/open_eye.jpg")
image_close = Image.open("/img/close_eye.jpg")
image_fire1 = Image.open("/img/fire1.jpg")
image_fire2 = Image.open("/img/fire2.jpg")

image_open = image_open.convert('1')
image_close = image_close.convert('1')
image_fire1 = image_fire1.convert('1')
image_fire2 = image_fire2.convert('1')

first_num = 1

while True:
    try:
        with open("expression.txt", "r") as f:
            first_num = int(f.readline().strip())
    except:
        first_num = firstnum
    if first_num == 1:
        disp.clear()
        disp.image(image_open)
        disp.display()
        time.sleep(1)
        disp.clear()
        disp.image(image_close)
        disp.display()
        time.sleep(1)
    elif first_num == 2:
        disp.clear()
        disp.image(image_fire1)
        disp.display()
        time.sleep(1)
        disp.clear()
        disp.image(image_fire2)
        disp.display()
        time.sleep(1)
