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
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)
    picam2.start()
    count = 0
    while True:
        count += 1
        filename = f'{FILE_NAME}{count}.png'
        picam2.capture_file(os.path.join(IMAGE_PATH,filename))
        if count >= 10:
            count = 0
        time.sleep(0.02)
    picam2.close()

if __name__ == '__main__':
    main()