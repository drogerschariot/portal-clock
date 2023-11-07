from playsound import playsound
import os
import gpiozero  # We are using GPIO pins
import time
import random

button_17 = gpiozero.Button(17) # GPIO17 connects to button 
button_26 = gpiozero.Button(26)
button_16 = gpiozero.Button(16)

sound_path = "sounds"
sounds_list = os.listdir(sound_path)

while True:
  if button_17.is_pressed or button_26.is_pressed or button_16.is_pressed:
    pick = random.randrange(1, len(sounds_list) - 1)
    print("Playing file : ", sounds_list[pick])
    playsound("sounds/" + sounds_list[pick])
    print("DONE")

  time.sleep(0.1)
