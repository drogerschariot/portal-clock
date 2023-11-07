from playsound import playsound
import multiprocessing
import os
import gpiozero  # We are using GPIO pins
import time
import random

button_17 = gpiozero.Button(17) # GPIO17 connects to button 
button_26 = gpiozero.Button(26)
button_16 = gpiozero.Button(16)

sound_path = "sounds"
sounds_list = os.listdir(sound_path)
pick = random.randrange(1, len(sounds_list) - 1)
p = multiprocessing.Process(target=playsound, args=("sounds/" + sounds_list[pick],))
p.start()
while True:
  print("Playing file : ", sounds_list[pick])
  print(p)
  time.sleep(1)
  if p.exitcode == 0:
    p = multiprocessing.Process(target=playsound, args=("sounds/" + sounds_list[pick],))
    p.start()
