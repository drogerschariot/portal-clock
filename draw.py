#!/usr/bin/env python
import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT
import subprocess
import json

pic = [
    (11,0), (12,1), (13,2)
]

def main():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False)
    device.contrast(16)

    toggle = False  # Toggle the second indicator every second
    while True:
        with canvas(device) as draw:
            for p in pic:
                draw.point(p, fill="white")
    sleep(10)

if __name__ == "__main__":
    main()
