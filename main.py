from gpiozero import LED
import time
 
relay = LED(17)

relay.on()
time.sleep(15)