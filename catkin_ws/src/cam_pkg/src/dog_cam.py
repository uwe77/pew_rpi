#!/usr/bin/env python3
import time
import sys, os
from picamera2 import Picamera2, Preview
import libcamera


IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            '../../../images')
FILE_NAME = "vision"

state_path = "../../../log/state.txt"
state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            state_path)
state = '0'

def main():
    state = '0'
    while True:
        if state == '0' or state == '2':
            init_size = os.path.getsize(state_path)
            while True:
                time.sleep(0.1)
                current_size = os.path.getsize(state_path)
                if current_size == init_size:
                    with open(state_path, 'r') as file:
                        state = file.read()
                    break
                init_size = current_size
        elif state == '1':
            picam2 = Picamera2()
            # picam2.start_preview(Preview.QTGL)
            preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
            preview_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
            picam2.configure(preview_config)
            picam2.start()
            count = 0
            while state == '1':
                count = (count % 2) + 1
                filename = f'{os.path.join(IMAGE_PATH,FILE_NAME)}{count}.png'
                init_size = os.path.getsize(filename)
                while True:
                    time.sleep(0.02)
                    current_size = os.path.getsize(filename)
                    if current_size == init_size:
                        break
                    init_size = current_size
                picam2.capture_file(filename)
                init_size = os.path.getsize(state_path)
                while True:
                    time.sleep(0.1)
                    current_size = os.path.getsize(state_path)
                    if current_size == init_size:
                        with open(state_path, 'r') as file:
                            state = file.read()
                        break
                    init_size = current_size
            picam2.close()

if __name__ == '__main__':
    main()