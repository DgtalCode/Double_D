# Untitled - By: hello - Пн окт 14 2019

import sensor, image, time
from math import degrees, atan

#(9, 40, -62, -13, -72, 34)

THRESH = [(70, 37, -56, -16, -47, 72)]
THRESHOLD = (11, 37, -28, 44, -51, 55)

#width and height of image
IMG_H = 240
IMG_W = 320

#region of interesting for marks finding
ROI = (0, 0, 320, 240)

#from (19, 31, -48, -17, -26, 31)
#to (19, 43, -50, -24, -26, 31)

#funtion for sorting array
def sort_key(val):
    return val[0]


#function that return 2 pairs of coordinates of one side of greenmark's blob
def normalise_corners(corners):
    n_corn = []

    #find min x,y
    for i in (0,1):
        a = corners[0]
        for c in corners:
            if c[i] < a[i]: a = c
        n_corn.append(a)

    #find max x,y
    for i in (0,1):
        a = corners[0]
        for c in corners:
            if c[i] > a[i]: a = c
        n_corn.append(a)

    n_corn.sort(key=sort_key)

    if n_corn[0][0] > n_corn[1][0]:
        n_corn[0][0], n_corn[1][0] = n_corn[1][0], n_corn[0][0]
    if n_corn[2][0] > n_corn[3][0]:
        n_corn[2][0], n_corn[3][0] = n_corn[3][0], n_corn[2][0]

    return n_corn

#calculates rotation of blob
def calculate_rotation(c):
    try:    t = (c[3][0] - c[2][0]) / (c[3][1] - c[2][1])
    except: t = 0
    return(degrees(atan(t)))

#rotates image
def rotate_image(img):
    a = 0
    a1 = 0
    f = False
    bls = img.find_blobs(THRESH, False, ROI)
    for i in range(len(bls)-1, -1, -1):
        if bls[i].area() < 1000:
            bls.pop(i)
    if bls:
        b = bls[0]
        for b1 in bls:
            if b.area() <= b1.area(): b = b1;
        c = b.min_corners()
        c = normalise_corners(c)
        a = calculate_rotation(c)
        lin = img.get_regression([THRESHOLD], False, (20, b.y(), IMG_W - 20, IMG_H - b.y()))
        img.draw_line(lin.x1(), lin.y1(), lin.x2(), lin.y2(), (255, 0, 0), 2)
        a1 = lin.theta() if lin else 0
        #a = (-a + 10) if (a1 > 90 and a > 0) else (-a - 10)
        if a > 25 and a1 > 90:
            a = -45 - (45 - a)
        if a < -25 and a1 < 75:
            a = 45 + (45 + a)
        #img.rotation_corr(0,0,a)
        f = True
        #print(a, a1)
    return a, a1, f

def marks_recognition(img, bls):
    a = 10
    left = False
    right = False
    try:
        for b in bls:
            clr_l = img.get_pixel(b.x() - a, b.cy())
            clr_r = img.get_pixel(b.x() + b.w() + a, b.cy())
            clr_d = img.get_pixel(b.cx(), b.y() - a)
            img.draw_circle(b.x() - a, b.cy(), 3, (0,0, 255), 2)
            img.draw_circle(b.x() + b.w() + a, b.cy(), 3, (0,0, 255), 2)
            img.draw_circle(b.cx(), b.y() - (a + 3), 3, (0,0, 255), 2)
            if bls and img:
                if sum(clr_d) < 150:
                    if sum(clr_l) < 150:    left = True
                    if sum(clr_r) < 150:    right = True
    except:
        pass
    if left and right:  return 2
    if left:     return 0
    if right:   return 1
    return 3

def marksss(img):
    a, a1, f = rotate_image(img)
    todo = 3
    #print(a)
    #bls = img.find_blobs([(15, 32, -55, -13, -40, 49)], False, ROI)
    try:
        if f:
            bls = img.find_blobs(THRESH, False)

            for i in range(len(bls)-1, -1, -1):
                if bls[i].w()*bls[i].h() < 1600:
                    bls.pop(i)

            if bls:
                bls.sort(key = sort_key)

                if len(bls) > 2:
                    m = bls[0]
                    ii = 0
                    for i, b in enumerate(bls):
                        if m.cy() > b.cy():
                            m = b
                            ii = i
                    bls.append(bls.pop(ii))

                i = 0
                for b in bls:
                    if b.area() > 1000:
                        i += 1
                        img.draw_rectangle(b.x(), b.y(), b.w(), b.h(), (255,100*i,50*i), 2)

                todo = marks_recognition(img, bls)
    except: pass
    return todo, a, a1

if __name__ == "__main__":
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_auto_gain(False, 15)
    sensor.skip_frames(time = 2000)

    clock = time.clock()

    while(True):
        clock.tick()
        img = sensor.snapshot()
        img.lens_corr(1.7, 1.3)
        todo, a, a1 = marksss(img)
        print(todo, a, a1)


    #img.binary([(19, 61, -50, -24, -26, 31)], False)
