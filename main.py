#!/bin/python3
from logipy import logi_led
import time, sys, signal
import psutil
from colour import Color
import ctypes

#Define Colors
red = Color("red")
green = Color("green")
grad = list(green.range_to(red,101))

#Catch CTRL+C / SIGINT
def signal_handler(sig,frame):
    print("EXIT")
    logi_led.logi_led_shutdown()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#Scale from 0.0/1.0 to 0/100
def led_color(r,g,b):
    logi_led.logi_led_set_lighting(int(r*100),int(g*100),int(b*100))

def start_up_led():
    led_color(1,0,0)
    time.sleep(.25)
    led_color(0,1,0)
    time.sleep(.25)
    led_color(0,0,1)
    time.sleep(.25)
    #led_color(.5,.5,.5)
    print("Init done")

logi_led.logi_led_init()
print(logi_led.led_dll)
time.sleep(1)
start_up_led()
print("Running CPU Monitor LED")
try:
    while True:
            #update color to current CPU percenage
            cpu_p = int(psutil.cpu_percent(interval=.25))
            col = grad[int(cpu_p)]
            sys.stdout.write(f"CPU %: {int(cpu_p)} COLOR %: RED: {int(col.red*100)} GREEN: {int(col.green*100)} BLUE: {int(col.blue*100)}\t\t\r")
            sys.stdout.flush()
            led_color(col.red,col.green,col.blue)
            #time.sleep(.3)
except Exception as e:
    print(f"ERROR: {e}")
    logi_led.logi_led_shutdown()
