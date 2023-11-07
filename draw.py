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

col1 = 0
col2 = 8
col3 = 16
col4 = 24

pic = [
(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (1,1), (1,6), (6,1), (6,6), (2,2), (2,5), (5,2), (5,5), (3,3), (3,4), (4,3), (4,4)
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

if __name__ == "__main__":
    main()
