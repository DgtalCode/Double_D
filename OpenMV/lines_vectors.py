# Untitled - By: hello - Сб окт 26 2019

import sensor, image, time
from math import asin, degrees, acos, atan

THRESHOLD = (0, 22, -17, 40, -45, 31)
red_thresh = [(0, 100, 52, 97, -1, 48)]

(0, 100, 34, 107, -8, 49)
IMG_W = 320
IMG_H = 240

ZERO_C = (IMG_W // 2, IMG_H)

up_roi = (0, 0, IMG_W, IMG_H // 2)
down_roi = (0, IMG_H // 2, IMG_W, IMG_H)

def sign(a):
    return 1 if a > 0 else -1

def get_max_blob(blobs):
    if blobs:
        mb = blobs[0]
        for b in blobs:
            if mb.area() < b.area():    mb = b
        return mb
    return -1

def get_line(img):
    up_blob = get_max_blob(img.find_blobs([THRESHOLD], False, up_roi))
    down_blob = get_max_blob(img.find_blobs([THRESHOLD], False, down_roi))
    full_blob = get_max_blob(img.find_blobs([THRESHOLD], False))

    try:    up_c = (up_blob.cx() - IMG_W // 2, IMG_H - up_blob.cy())
    except: pass
    try:    down_c = (down_blob.cx() - IMG_W // 2, IMG_H - down_blob.cy())
    except: pass
    try:    full_c = (full_blob.cx() - IMG_W // 2, IMG_H - full_blob.cy())
    except: pass

    #img.draw_line(up_blob.cx(), up_blob.cy(), ZERO_C[0], ZERO_C[1], (255,0,0), 2)
    #img.draw_line(down_blob.cx(), down_blob.cy(), ZERO_C[0], ZERO_C[1], (255,0,0), 2)

    a1, a2, a3 , red_flag= 0, 0, 0, False
    try:
        a1 = degrees(atan(up_c[1] / up_c[0]))
        a1 = sign(a1)*90-a1
    except: pass
    try:
        a2 = degrees(atan(down_c[1] / down_c[0]))
        a2 = sign(a2)*90-a2
    except: pass
    try:
        a3 = degrees(atan(full_c[1] / full_c[0]))
        a3 = sign(a3)*90-a3
    except: pass

    return (a1,a2,a3)

if __name__ == "__main__":
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)

    clock = time.clock()

    while(True):
        clock.tick()
        img = sensor.snapshot()
        print(get_line(img))

