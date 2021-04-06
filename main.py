#!/usr/bin/python3
import os
from time import sleep

import evdev
import pygame
from pygame.locals import *

import scrape

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

#Display to Framebuffer
os.putenv('SDL_FBDEV', '/dev/fb1')

#Init pygame, 3.5" touchscreen
pygame.init()
surface_size = (480, 320)

#Touchscreen map
#THIS MAY BE WRONG
#tftOrig = (3750, 180)
#tftEnd = (150, 3750)
#tftDelta = (tftEnd[0] - tftOrig[0], tftEnd[1] - tftOrig[1])
#tftAbsDelta = (abs(tftEnd [0] - tftOrig [0]), abs(tftEnd [1] - tftOrig [1]))

# Create touchscreen object using evdev
touch = evdev.InputDevice('/dev/input/touchscreen')

pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((surface_size))
lcd.fill((BLACK))
pygame.display.update()

weather, covid = scrape.get_data()

font_title = pygame.font.Font(None, 50)
font_regular = pygame.font.Font(None, 20)

#touch_buttons = {'TEST':(80,60), 'BUM':(240,60), 'MINGE':(80,180), 'QUIM':(240,180)}

text_surface = font_title.render("Jersey Covid Data", True, ORANGE)
rect = text_surface.get_rect(center=20,20)
lcd.blit(text_surface, rect)


text_surface = font_regular.render(covid[0])
rect = text_surface.get_rect(center=20,50)
lcd.blit(text_surface, rect)

text_surface = font_regular.render(covid[1])
rect = text_surface.get_rect(center=40,50)
lcd.blit(text_surface, rect)

#for k,v in touch_buttons.items():
#    text_surface = font_big.render('%s'%k, True, WHITE)
#    rect = text_surface.get_rect(center=v)
#    lcd.blit(text_surface, rect)

pygame.display.update()


# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()
# Prints some info on how evdev sees our input device
print(touch)
# Even more info for curious people
#print(touch.capabilities())

# Here we convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
def getPixelsFromCoordinates(coords):
    # TODO check divide by 0!
    if tftDelta [0] < 0:
        x = float(tftAbsDelta [0] - coords [0] + tftEnd [0]) / float(tftAbsDelta [0]) * float(surface_size [0])
    else:
        x = float(coords [0] - tftOrig [0]) / float(tftAbsDelta [0]) * float(surface_size [0])
    if tftDelta [1] < 0:
        y = float(tftAbsDelta [1] - coords [1] + tftEnd [1]) / float(tftAbsDelta [1]) * float(surface_size [1])
    else:
        y = float(coords [1] - tftOrig [1]) / float(tftAbsDelta [1]) * float(surface_size [1])
    return (int(x), int(y))


#Main loop
while True:
#    state=4
#
#    for event in touch.read_loop():
#        if event.type == evdev.ecodes.EV_ABS:
#            print(state)
#            sleep(0.2)

pygame.quit()
quit()
