# diorama.py controls the synchronized LED effects and slide show for the 390th diorama.
#
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)

import time
from subprocess import call, DEVNULL
from neopixel import *


# LED strip configuration:
LED_COUNT      = 18      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 400000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


ON_COLOR = Color(255, 0, 0)
OFF_COLOR = Color(0, 0, 0)

SLIDE_COUNT = 10
LED_PATTERNS = {
    0: [], # This is the startup pattern, not associated with any slide.
    1: [5,6,7,8], # LEDs 5, 6, and 7 should be lit for slide 1.
    # Since there is no pattern for slide 2, the pattern for slide 1 will persist.
    3: [12, 14], # LEDs 12 and 14 should be lit for slide 3. 
    4: [], # All the LEDs should be off for slide 4.
    # Slides 5, 6, 7, 8, and 9 will also have all LEDs off.
    10: [1,7,8,18], # LEDs 1, 7, 8, and 18 should be lit for slide 10.
}

def show_slide_leds(strip, slidenum):
    if slidenum in LED_PATTERNS:
        brightleds = LED_PATTERNS[slidenum]
        for i in range(strip.numPixels()):
            color = ON_COLOR if i+1 in brightleds else OFF_COLOR
            strip.setPixelColor(i, color)
        strip.show()
 
def show_slide_image(slidenum):
    call(["pkill", "fbi"])
    filename = "slides/Slide{:02}.JPG".format(slidenum)
    cmd = ["fbi", "--autozoom", "--vt", "1", "--noverbose", filename]
    call(cmd, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

def show_slide(strip, slidenum):
    show_slide_image(slidenum)
    show_slide_leds(strip, slidenum)

if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')

    while True:
        show_slide(strip, 0)
        for s in range(SLIDE_COUNT):
            show_slide(strip, s+1)
            time.sleep(2)

