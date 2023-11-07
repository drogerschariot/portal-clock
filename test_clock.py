#!/usr/bin/env python
import gpiozero  # We are using GPIO pins
import time
import random
import os
import datetime
from playsound import playsound
from hour import hour_frames
from alarm import alarm_frames, logo
import multiprocessing

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

button_17 = gpiozero.Button(17) # GPIO17 connects to button 
button_26 = gpiozero.Button(26)
button_16 = gpiozero.Button(16)

sounds_list = [
    "-bw_sp_a2_core_lift_nags04.mp3",
    "-chellgladoswakeup06.mp3",
    "-sp_a2_bridge_intro01.mp3",
    "-sp_a2_bts5_hack11.mp3",
    "-coop_vault_intro01.mp3",
    "-sp_a2_bts5_science_fair03.mp3",
    "-gladosbattle_xfer17.mp3",
    "-bw_sp_a2_core_history_response05.mp3",
    "-fgbrvtrap05.mp3",
    "-bw_finale04_pre_pipebreak14.mp3",
    "-sp_a1_wakeup_catwalk03.mp3",
    "-taunt_somersault02.mp3",
    "-sp_laser_powered_lift_completion02.mp3",
    "-sp_sabotage_factory_defect_chat01.mp3",
    "-a4_recapture04.mp3",
    "-bw_a4_2nd_first_test_solve05.mp3",
    "-sp_a2_tube_ride02.mp3",
    "-fifties_fifth_test_complete08.mp3",
    "-bb_reactor07.mp3",
    "-sp_a2_trust_fling04.mp3"

]

def run_alarm(device, fps=0.4):
    count = 0
    print("PLAYING ALARM")
    music_thread = multiprocessing.Process(target=playsound, args=("sounds/portal_radio_song.mp3",))
    music_thread.start()
    while count < 3:
        for p in alarm_frames:
            while True:
                with canvas(device) as draw: 
                    draw.point(p, fill="white")
                if music_thread.exitcode == 0:
                    music_thread = multiprocessing.Process(target=playsound, args=("sounds/portal_radio_song.mp3",))
                    music_thread.start()
                    count = count + 1
                if button_17.is_pressed or button_16.is_pressed:
                    music_thread.terminate()
                    print("NO SNOOZE!")
                    pick = random.randrange(1, len(sounds_list) - 1)
                    music_thread = multiprocessing.Process(target=playsound, args=("sounds/" + sounds_list[pick],))
                    music_thread.start()
                    return False
                if button_26.is_pressed:
                    music_thread.terminate()
                    print("SNOOOZE!")
                    return True
                time.sleep(fps)
                break
        
    music_thread.terminate()
    print("ALARM TIMEOUT")
    return False

def hour_animation(device, hour, fps=0.4):
    current_frame = 0
    for p in hour_frames:
        while True:
            with canvas(device) as draw: 
                print(p)
                text(draw, (0, 1), str(hour) if current_frame < 15 else str((hour + 1)), fill="white", font=proportional(CP437_FONT))
                draw.point(p, fill="white")
            time.sleep(fps)
            current_frame = current_frame + 1
            break

def set_alarm(device, ALARM_TIME):
    # give some time to not go back
    time.sleep(1)
    print ("Current Alarm:" + ALARM_TIME)
    hours = int(ALARM_TIME.split(':')[0])
    minutes = int(ALARM_TIME.split(':')[1])
    ampm = ALARM_TIME.split(':')[3]

    with canvas(device) as draw:
        text(draw, (0, 1), str(hours), fill="white", font=proportional(TINY_FONT))
        text(draw, (9, 1), ":", fill="white", font=proportional(TINY_FONT))
        text(draw, (11, 1), str(minutes), fill="white", font=proportional(TINY_FONT))
        text(draw, (20, 1), ampm, fill="white", font=proportional(TINY_FONT))

    while True:
        if button_26.is_pressed:
            if hours == 12:
                hours = 1
                if ampm == "PM":
                    ampm = "AM"
                else:
                    ampm = "PM"
            else:
                hours = hours + 1

        if button_16.is_pressed:
            if minutes == 59:
                minutes = 0
            else:
                minutes = minutes + 1
        
        with canvas(device) as draw:
            text(draw, (0, 1), str(hours), fill="white", font=proportional(TINY_FONT))
            text(draw, (9, 1), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (11, 1), str(minutes) if minutes > 9 else "0"+str(minutes), fill="white", font=proportional(TINY_FONT))
            text(draw, (20, 1), ampm, fill="white", font=proportional(TINY_FONT))
        time.sleep(0.1)

        if button_17.is_pressed:
            if minutes > 9:
                minutes = str(minutes)
            else:
                minutes = "0"+str(minutes)
            if hours > 9:
                hours = str(hours)
            else:
                hours = "0"+str(hours)
                
            return hours+":"+minutes+":01:"+ampm
            
    

def start_logo(device):
    hourstime = datetime.datetime.now().strftime('%H')
    mintime = datetime.datetime.now().strftime('%M')

    music_thread = multiprocessing.Process(target=playsound, args=("sounds/valve_intro_sound.mp3",))
    music_thread.start()

    for x_cord in range(-10,30):
        print("Range "+str(x_cord))
        for p in logo:
            while True:
                with canvas(device) as draw:
                    draw.point([((1+x_cord),0), ((2+x_cord),0), ((3+x_cord),0), ((4+x_cord),0), ((5+x_cord),0), ((6+x_cord),0), ((0+x_cord),1), ((0+x_cord),2), ((0+x_cord),3), ((0+x_cord),4), ((0+x_cord),5), ((0+x_cord),6), ((1+x_cord),7), ((2+x_cord),7), ((3+x_cord),7), ((4+x_cord),7), ((5+x_cord),7), ((6+x_cord),7), ((7+x_cord),1), ((7+x_cord),2), ((7+x_cord),3), ((7+x_cord),4), ((7+x_cord),5), ((7+x_cord),6), ((1+x_cord),1), ((1+x_cord),6), ((6+x_cord),1), ((6+x_cord),6), ((2+x_cord),2), ((2+x_cord),5), ((5+x_cord),2), ((5+x_cord),5), ((3+x_cord),3), ((3+x_cord),4), ((4+x_cord),3), ((4+x_cord),4)], fill="white")
                time.sleep(0.004)
                break

def minute_change(device):
    hours = datetime.datetime.now().strftime('%H')
    minutes = datetime.datetime.now().strftime('%M')

    def helper(current_y):
        with canvas(device) as draw:
            text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (17, current_y), minutes, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
    for current_y in range(1, 9):
        helper(current_y)
    minutes = datetime.datetime.now().strftime('%M')
    for current_y in range(9, 1, -1):
        helper(current_y)

def main():
    ALARM_TIME = "08:33:01:AM"
    ALARM_SET = False
    SNOOZE_SET = False
    SNOOZE_TIME = datetime.datetime.now()
    SNOOZE_COUNTER = 1

    # Setup for Banggood version of 4 x 8x8 LED Matrix (https://bit.ly/2Gywazb)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False)
    device.contrast(16)

    # Start the clock
    start_logo(device)

    blinky = False  # Blink every second
    while True:
        blinky = not blinky
        sec = datetime.datetime.now().second
        mins = datetime.datetime.now().minute
        hour = datetime.datetime.now().hour

        # Trigger Alarm
        print("ALARM:"+str(ALARM_SET)+" "+ALARM_TIME +"="+datetime.datetime.now().strftime('%I:%M:%S:%p')+ " SNOOZE:"+ str(SNOOZE_SET)+" SNOOZE TIME: "+str(SNOOZE_TIME.strftime('%I:%M:%S:%p')))
        if ALARM_SET or SNOOZE_SET:
            if ALARM_TIME == datetime.datetime.now().strftime('%I:%M:%S:%p') or SNOOZE_TIME.strftime('%I:%M:%S:%p') == datetime.datetime.now().strftime('%I:%M:%S:%p'):
                
                SNOOZE_SET = run_alarm(device)
                if SNOOZE_SET:
                    SNOOZE_TIME = datetime.datetime.strptime(ALARM_TIME, '%I:%M:%S:%p')
                    SNOOZE_TIME = SNOOZE_TIME + datetime.timedelta(minutes=(1 * SNOOZE_COUNTER))
                    SNOOZE_COUNTER = SNOOZE_COUNTER + 1
                    time.sleep(1)
                else:
                    SNOOZE_COUNTER = 1
                    time.sleep(1)

        # Set Alarm
        if button_17.is_pressed:
            ALARM_TIME = set_alarm(device, ALARM_TIME)
            print(ALARM_TIME)
            time.sleep(1)

        # Enable/Disable Alarm
        if button_16.is_pressed:
            if ALARM_SET:
                ALARM_SET = False
            else:
                ALARM_SET = True
            time.sleep(0.5)

        # Hours/Minutes animations 
        if mins == 30 and sec == 20:
            hour_animation(device, hour, 0.4)
        elif sec == 59:
            minute_change(device)
        else:
            hours = datetime.datetime.now().strftime('%H')
            minutes = datetime.datetime.now().strftime('%M')
            with canvas(device) as draw:
                text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
                text(draw, (15, 1), ":" if blinky else " ", fill="white", font=proportional(TINY_FONT))
                text(draw, (17, 1), minutes, fill="white", font=proportional(CP437_FONT))
                if ALARM_SET:
                    draw.point([(31,0), (31,7)], fill="white")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
