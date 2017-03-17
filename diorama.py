# diorama.py controls the synchronized LED effects and slide show for the 390th diorama.
# Adrian Boyko for Xerocraft

import time
import pygame
from neopixel import *

# LED strip configuration:
LED_COUNT      = 54      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 400000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

ON_COLOR = Color(255, 0, 0)
OFF_COLOR = Color(0, 0, 0)

SLIDE_COUNT = 10
LED_PATTERNS = {
    1: [5,6,7,8], # LEDs 5, 6, and 7 should be lit for slide 1.
    # Since there is no pattern for slide 2, the pattern for slide 1 will persist.
    3: [12, 14], # LEDs 12 and 14 should be lit for slide 3. 
    4: [], # All the LEDs should be off for slide 4.
    5: [22, 23, 24, 25, 26, 27],
    6: [54, 53, 52, 51, 50],
    10: [1,7,8,18], # LEDs 1, 7, 8, and 18 should be lit for slide 10.
}

def show_slide_leds(strip, slidenum):
    if slidenum in LED_PATTERNS:
        brightleds = LED_PATTERNS[slidenum]
        for i in range(strip.numPixels()):
            color = ON_COLOR if i+1 in brightleds else OFF_COLOR
            strip.setPixelColor(i, color)
        strip.show()
 
def show_slide_image(screen, slidenum):
    filename = "slides/Slide{:02}.JPG".format(slidenum)
    slide = pygame.image.load(filename)    
    slide_rect = slide.get_rect()

    # Resize the images to the screen.
    # For some reason, all provided images are 960x576, so we're always scaling up. 
    scale_x = screen.get_width() / slide_rect.width
    scale_y = screen.get_height() / slide_rect.height
    scale = min(scale_x, scale_y)
    scaled_width = int(scale * slide_rect.width)
    scaled_height = int(scale * slide_rect.height)
    scaled_size = (scaled_width, scaled_height)
    slide = pygame.transform.smoothscale(slide, scaled_size)

    # Since the scaled image probably isn't a perfect fit, center it.
    delta_x = (screen.get_width() - scaled_width) / 2.0
    delta_y = (screen.get_height() - scaled_height) / 2.0
    slide_rect.move_ip(delta_x, delta_y)

    # Blit the modified slide
    black = 0, 0, 0
    screen.fill(black)
    screen.blit(slide, slide_rect)
    pygame.display.flip()

def show_slide(strip, screen, slidenum):
    show_slide_image(screen, slidenum)
    show_slide_leds(strip, slidenum)

if __name__ == '__main__':

    # Initialize the neopixel strip.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, OFF_COLOR)

    # Initialize pygame for image display.
    pygame.init()
    pygame.mouse.set_visible(0)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size)

    while True:
        for s in range(SLIDE_COUNT):
            show_slide(strip, screen, s+1)
            time.sleep(5)

