import cv2
from subprocess import Popen, PIPE
from PIL import Image
import numpy as np
import argparse


def command_option():
    parser = argparse.ArgumentParser(description='specify input and output device')
    parser.add_argument('--input_video_num', type=int,
                        help='input video device number. ex) if input is /dev/video0 then the value is 0', default=0)
    parser.add_argument('--output_video_dev', type=str,
                        help='input video device. ex) /dev/video2', default="/dev/video2")

    return parser.parse_args()


def gray_scale(frame):
    result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return result


def edge(frame):
    result = cv2.Canny(im, 100, 200)

    return result


def bitwise_not(frame):
    result = cv2.bitwise_not(frame)

    return result


if __name__ == "__main__":
    opts = command_option()
    input = opts.input_video_num
    output = opts.output_video_dev
    cap = cv2.VideoCapture(input)

    p = Popen(['ffmpeg', '-y', '-i', '-', '-pix_fmt', 'yuyv422', '-f', 'v4l2', output], stdin=PIPE)

    try:
        mode = 0
        while True:
            ret, im = cap.read()
            if mode == 0:
                pass
            elif mode == 1:
                im = gray_scale(im)
            elif mode == 2:
                im = edge(im)
            elif mode == 3:
                im = bitwise_not(im)

            cv2.imshow("frame", im)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(np.uint8(im))
            im.save(p.stdin, 'JPEG')
            k = cv2.waitKey(1) & 0xFF
            if k == ord("0"):
                mode = 0
            elif k == ord("1"):
                mode = 1
            elif k == ord("2"):
                mode = 2
            elif k == ord("3"):
                mode = 3
    p.stdin.close()
    p.wait()
