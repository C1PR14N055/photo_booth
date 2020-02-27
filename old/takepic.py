from datetime import datetime
import os
import pygame
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from PIL import Image

PATH = "/home/pi/selphone/"
IMG_FOLDER = PATH + "pics/"
PIC_TIMER = 10
# pin 14 bcm to GND
PIN_BUTTON = 14

camera = None
sound = None

def init():
    global camera
    # button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #sound
    pygame.mixer.init()
    pygame.mixer.music.load(PATH + "shutter.mp3")
    # camera
    camera = PiCamera(resolution=(1080, 1920), framerate=30, sensor_mode=2)
    # take_pic()
    loop()

def take_pic():
    camera.resolution = (1080, 1920)
    camera.rotation = 90
    camera.hflip = True
    camera.start_preview()
    timer()
    img = "%sIMG%s.jpg" % (IMG_FOLDER, datetime.now().strftime("_%d-%m-%Y-%H:%M:%S"))
    camera.capture(img)
    os.system("convert -flop -auto-gamma -auto-level -normalize '%s' '%s' &" % (img, img))
    thank_you(img)
    camera.stop_preview()

def timer():
    pygame.mixer.music.play()
    time.sleep(1)
    camera.annotate_text_size = 160 
    for i in range(PIC_TIMER, -1, -1):
        if i > 0:
            camera.annotate_text = "\n\n\n\n\n%d" % i
            time.sleep(1)
        else:
            camera.annotate_text = ""

def thank_you(img_uri):
    bck = Image.open(img_uri)
    thx = Image.open(PATH + "/assets/thanks.png")
    ovr = Image.new("RGB", (
        ((bck.size[0] + 31) // 32) * 32,
        ((bck.size[1] + 15) // 16) * 16,
    ))
    ovr.paste(bck, (0, 0))
    ovr.paste(thx, (bck.size[0] / 2 - thx.size[0] / 2, 100))
    o = camera.add_overlay(ovr.tobytes(), size=ovr.size)
    o.layer = 3
    time.sleep(3)
    camera.remove_overlay(o)

def loop():
    while True:
        if GPIO.input(PIN_BUTTON) == True:
            take_pic()

init()