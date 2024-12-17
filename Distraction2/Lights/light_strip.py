# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random

length = 10
pixels = neopixel.NeoPixel(board.D10, length)
sleep_time = 0.18

# clear lights
pixels.fill((0,0,0))

# Police lights
for count in range(6):
     # Flash halves 3 times
    for num in range(5):

        # Half red
        pixels.fill((0,0,0))
        for i in range(int(length/2)):
            pixels[i + int(length/2)] = (200,0,0)

        # Wait
        time.sleep(sleep_time)

        # Other half blue
        pixels.fill((0,0,0))
        for i in range(int(length/2)):
            pixels[i] = (0,0,200)

        # Wait
        time.sleep(sleep_time)


    # Takedown pattern 3 times
    for num in range(5):
        
        # PHASE 1
        # First 2 red
        pixels[9] = (200,0,0)
        pixels[8] = (200,0,0)

        # Next 2 white
        pixels[7] = (200,200,200)
        pixels[6] = (200,200,200)

        # Next 2 black
        pixels[5] = (0,0,0)
        pixels[4] = (0,0,0)

        # Next 2 blue
        pixels[3] = (0,0,200)
        pixels[2] = (0,0,200)

        # Next 2 white
        pixels[1] = (200,200,200)
        pixels[0] = (200,200,200)

        # Wait before next phase
        time.sleep(sleep_time)


        # PHASE 2
        # First 2 black
        pixels[9] = (0,0,0)
        pixels[8] = (0,0,0)

        # Next 2 white
        pixels[7] = (200,200,200)
        pixels[6] = (200,200,200)

        # Next 2 blue
        pixels[5] = (0,0,200)
        pixels[4] = (0,0,200)

        # Next 2 black
        pixels[3] = (0,0,0)
        pixels[2] = (0,0,0)

        # Next 2 red
        pixels[1] = (200,00,0)
        pixels[0] = (200,0,0)

        # Wait before next phase
        time.sleep(sleep_time)

# clear lights
pixels.fill((0,0,0))