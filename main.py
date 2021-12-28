#!/usr/bin/env python3

import RPi.GPIO as GPIO
from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime
import requests

data = {'time': datetime.today(), 'device': 'landscape'}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 27
GPIO.setup(GPIO_PIN, GPIO.OUT)

city = lookup("San Diego", database())
s = sun(city.observer, date=date.today())
sunrise = s["sunrise"]
sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
#sunset = s["sunset"] - timedelta(hours=8) # FOR TESTING ONLY
sunset = s["sunset"]
sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))

if sunset.time() < datetime.now().time():
    if GPIO.input(GPIO_PIN):
        quit()
    else:
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        data['setting'] = True
else:
    if not GPIO.input(GPIO_PIN):
        quit()
    else:
        GPIO.output(GPIO_PIN, GPIO.LOW)
        data['setting'] = False
        
# # Send new data to database
requests.post('http://192.168.86.31/landscape/update-state', params=data)
