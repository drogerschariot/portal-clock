import gpiozero  # We are using GPIO pins
import time

button_17 = gpiozero.Button(17) # GPIO17 connects to button 
button_26 = gpiozero.Button(26)
button_16 = gpiozero.Button(16)

while True:
  if button_17.is_pressed:
    print("Button 17 is pressed!")
  elif button_26.is_pressed:
    print("Button 26 is pressed!")
  elif button_16.is_pressed:
    print("Button 16 is pressed!")
  
  time.sleep(0.1)
