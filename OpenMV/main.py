# Untitled - By: hello - Ср сен 25 2019

import sensor, image, time
from pyb import LED, Pin

#from lines_nonzero_vertical import get_line
from lines_vectors import get_line
import marks
from pyb import UART

uart = UART(3, 9600, timeout_char=1000)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

def get_max_blob(blobs):
    if blobs:
        mb = blobs[0]
        for b in blobs:
            if mb.area() < b.area():    mb = b
        return mb
    return -1

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    #img.lens_corr(1.8)
    try:
        todo, angle, angle1 = marks.marksss(img)

        a1, a2, a3 = get_line(img)


        print(":%i/%i/%i/%i/%i/;" % (a1, a2, a3, todo, angle))

        #uart.write(":%i/%i/%i/%i/%i/;" % (a1, a2, a3, todo, angle))
    except:
        pass
