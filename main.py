#!/usr/bin/python3

import os
import sys
import io
from time import sleep

import evdev
import pygame
from pygame.locals import *

import scrape

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 20, 200)

#Page 1 data script
def display_page1(lcd, covid):

    lcd.fill((BLACK))
    pygame.display.update()

    font_title = pygame.font.Font(None, 50)
    font_regular = pygame.font.Font(None, 35)

    text_surface = font_title.render("Jersey Covid Data", True, ORANGE)
    rect = text_surface.get_rect(topleft=(30,20))
    lcd.blit(text_surface, rect)

    text_surface = font_regular.render("Date: "+covid[0]+" Active cases: "+covid[1], True, WHITE)
    rect = text_surface.get_rect(topleft=(30,55))
    lcd.blit(text_surface, rect)

    pygame.display.update()

#Page 2 data script
def display_page2(lcd, weather):

    lcd.fill((BLACK))
    pygame.display.update()

    font_title = pygame.font.Font(None, 50)
    font_regular = pygame.font.Font(None, 35)

    text_surface = font_title.render("Jersey Weather", True, ORANGE)
    rect = text_surface.get_rect(topleft=(30,20))
    lcd.blit(text_surface, rect)

    text_surface = font_regular.render("Max: "+weather[0]+"  Min: "+weather[1], True, WHITE)
    rect = text_surface.get_rect(topleft=(30,55))
    lcd.blit(text_surface, rect)

    text_surface = font_title.render("Current: "+weather[2], True, BLUE)
    rect = text_surface.get_rect(topleft=(30,100))
    lcd.blit(text_surface, rect)

    #weather_icon = pygame.image.load(img)
    #weather_icon.convert()
    #rect = weather_icon.get_rect(topleft=(100,100))
    #lcd.blit(weather_icon, rect)


    pygame.display.update()

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

# convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
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


def main():

    #Display to Framebuffer
    os.putenv('SDL_FBDEV', '/dev/fb1')

    #Init pygame, 3.5" touchscreen
    pygame.init()
    surface_size = (480, 320)


    # Create touchscreen object using evdev, grab mouse
    touch = evdev.InputDevice('/dev/input/touchscreen')
    touch.grab()

    pygame.mouse.set_visible(False)
    lcd = pygame.display.set_mode((surface_size))
    lcd.fill((BLACK))
    pygame.display.update()

    weather, covid = scrape.get_data()

    #I think it's better to have the icon png's in a file
    #and select from the scraped img url
    #rather than downloading the images every time
    print (weather[4])
    display_page1(lcd, covid)

    count = 0

    while True:
        for event in touch.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                count += 1
                print(count)
                if count == 20:
                    print("QUIT")
                    pygame.quit()
                    sys.exit()
                elif (count % 4) == 0:
                    display_page2(lcd, weather)
                    sleep(1)
                elif (count % 2) == 0:
                    display_page1(lcd, covid)
                    sleep(1)
                else:
                    print("pass")


if __name__ == "__main__":
    main()









    #Touchscreen map
    #THIS MAY BE WRONG
    #tftOrig = (3750, 180)
    #tftEnd = (150, 3750)
    #tftDelta = (tftEnd[0] - tftOrig[0], tftEnd[1] - tftOrig[1])
    #tftAbsDelta = (abs(tftEnd [0] - tftOrig [0]), abs(tftEnd [1] - tftOrig [1]))


    #for k,v in touch_buttons.items():
    #    text_surface = font_big.render('%s'%k, True, WHITE)
    #    rect = text_surface.get_rect(center=v)
    #    lcd.blit(text_surface, rect)
