#!/usr/bin/env python3
import time
import sys, os
from picamera2 import Picamera2, Preview


IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            '../../../images')
FILE_NAME = "vision"

def main():
    picam2 = Picamera2()
    # picam2.start_preview(Preview.QTGL)
    preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(preview_config)
    picam2.start()
    count = 0
    while True:
        count = (count % 10) + 1
        filename = f'{os.path.join(IMAGE_PATH,FILE_NAME)}{count}.png'
        init_size = os.path.getsize(filename)
        while True:
            time.sleep(0.02)
            current_size = os.path.getsize(filename)
            if current_size == init_size:
                break
            init_size = current_size
        picam2.capture_file(filename)
        time.sleep(0.02)
    picam2.close()

if __name__ == '__main__':
    main()