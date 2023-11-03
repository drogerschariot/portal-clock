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

def main():
    # Setup for Banggood version of 4 x 8x8 LED Matrix (https://bit.ly/2Gywazb)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False)
    device.contrast(16)

    toggle = False  # Toggle the second indicator every second
    while True:
      ## call date command ##
      cmd = 'sensors -j | jq \'.["cpu_thermal-virtual-0"]["temp1"]["temp1_input"]\''
      # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
      # (output, err) = p.communicate()
      # p_status = p.wait()
      output = subprocess.getoutput(cmd)

      with canvas(device) as draw:
        text(draw, (0, 0), str(output) +"C", fill="red", font=proportional(TINY_FONT))
        time.sleep(5)

if __name__ == "__main__":
    main()
