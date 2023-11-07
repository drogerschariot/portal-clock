#!/usr/bin/env python
import gpiozero  # We are using GPIO pins
import time
import random
import os
from datetime import datetime
from playsound import playsound
from hour import hour_frames
from alarm import alarm_frames

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

def hour_animation(device, fps=0.4):
    for p in hour_frames:
        while True:
            with canvas(device) as draw: 
                print(p)
                text(draw, (0, 1), "10", fill="white", font=proportional(CP437_FONT))
                draw.point(p, fill="white")
            time.sleep(fps)
            break
def alarm_animation(device, fps=0.6):
    while True:
        for p in alarm_frames:
            with canvas(device) as draw: 
                print(p)
                draw.point(p, fill="white")
            time.sleep(fps)


def main():
  serial = spi(port=0, device=0, gpio=noop())
  device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False)
  device.contrast(16)
  alarm_animation(device)

#   hour_animation(device)
    # serial = spi(port=0, device=0, gpio=noop())
    # device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False)
    # device.contrast(16)

    # toggle = False  # Toggle the second indicator every second
    # while True:
    #     with canvas(device) as draw:
    #         for p in pic:
    #             draw.point(p, fill="white")

if __name__ == "__main__":
    main()
