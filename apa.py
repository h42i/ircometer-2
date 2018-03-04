from machine import Pin
from apa102 import APA102

clock = Pin(13, Pin.OUT)     # set GPIO14 to output to drive the clock
data = Pin(12, Pin.OUT)      # set GPIO13 to output to drive the data
apa = APA102(clock, data, 2) # create APA102 driver on the clock and the data pin for 8 pixels

def amplitude(p):
    r = int(p * 255)
    g = int((1-p) * 255)
    apa[0] = (r, g, 0, 31)
    apa[1] = (r, g, 0, 31)
    apa.write()
    apa.write()

def color_l(r, g, b, bri):
    apa[1] = (r, g, b, bri)
    apa.write()
    apa.write()

def color_r(r, g, b, bri):
    apa[0] = (r, g, b, bri)
    apa.write()
    apa.write()

def color(r, g, b, bri):
    apa[0] = (r, g, b, bri)
    apa[1] = (r, g, b, bri)
    apa.write()
    apa.write()

#r, g, b, brightness = apa[0] # get first pixel colour
